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
    Dependency to get currnet authenticated user base on the token.
    Decodes the token, retrieves the user ID, and fetches the user form the repository.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = decode_access_token(token)
    if token is None:
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

    print(f"Successfully authenticated user ID: {user.user_id} from token. ")
    return user


TokenDep = Annotated[int, Depends(oauth2_scheme)]
Current_user = Annotated[UserModel, Depends(get_current_user)]
