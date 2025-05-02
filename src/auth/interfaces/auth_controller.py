from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from auth.infrastructure.models import AuthenticateUserRequest, TokenModel
from auth.interfaces.dependencies import AuthenticateUser
from shared.domain.base_errores import AuthorizationError, EntityNotFoundError

router = APIRouter()


@router.post(
    "/token",
    response_model=TokenModel,
    summary="Login to get access token",
    description="Authenticate user with username (email) and password, returns JWT token.",
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authenticate_use_case: AuthenticateUser,
):
    """
    Authenticates a user and returns an access token.

    This endpoint handles user authentication using the OAuth2 password flow. It validates
    the provided credentials and returns a JWT token if successful.
    """
    auth_request = AuthenticateUserRequest(
        username=form_data.username,
        password=form_data.password,
    )
    try:
        token = await authenticate_use_case.execute(auth_request)
        return TokenModel(**token)
    except (AuthorizationError, EntityNotFoundError) as e:
        print(f"Unauthorized, wrong credentials {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        print(f"Unexpected error during authentication: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred during authentication.",
        )
