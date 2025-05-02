from http.client import HTTPException
from typing import Annotated

from fastapi import status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer

from auth.application.authenticate_user import AuthenticateUserUseCase
from shared.application.security import decode_access_token
from users.infraestructure.models import UserModel
from users.infraestructure.repositories import UserRepository
from users.interfaces.dependencies import get_user_repository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_authenticate_user_use_case(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> AuthenticateUserUseCase:
    """
    Dependency injection for the AuthenticateUserUseCase.
    """
    return AuthenticateUserUseCase(user_repo)


AuthenticateUser = Annotated[
    AuthenticateUserUseCase, Depends(get_authenticate_user_use_case)
]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserModel:
    """
    Dependency to get the current authenticated user based on the token.

    This function validates the provided JWT token, decodes it to extract user information,
    and retrieves the corresponding user from the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = decode_access_token(token)
    if token_data is None:
        print("Token decode failed or token invalid.")
        raise credentials_exception

    user_id = token_data.get("sub")
    if user_id is None:
        print("Token does not contain user ID.")
        raise credentials_exception
    try:
        user_id = int(user_id)
    except ValueError:
        print(f"Invalid user ID format in token's 'sub' claim: {user_id}")
        raise credentials_exception

    user = await user_repo.get_user_by_id(user_id)
    if user is None:
        print(f"User with ID {user_id} not found.")
        raise credentials_exception

    print(f"Successfully authenticated user ID: {user.user_id} from token.")
    return user


TokenDep = Annotated[str, Depends(oauth2_scheme)]
"""
Annotated type for injecting the OAuth2 token dependency.

This annotation is used in FastAPI endpoints to automatically resolve and inject
the JWT token from the request headers.
"""

Current_user = Annotated[UserModel, Depends(get_current_user)]
"""
Annotated type for injecting the current authenticated user dependency.

This annotation is used in FastAPI endpoints to automatically resolve and inject
the authenticated user model instance.
"""
