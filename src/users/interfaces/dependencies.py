from typing import Annotated

from fastapi import Depends

from shared.infrastructure.dependencies import DbSession
from users.infraestructure.repositories import UserRepository


def get_user_repository(session: DbSession) -> UserRepository:
    """
    Provides a UserRepository instance with a database session.

    This function is used as a dependency in FastAPI to inject a `UserRepository`
    instance into endpoints or services that require it.

    Args:
        session (DbSession): The database session to be used by the repository.

    Returns:
        UserRepository: A new instance of `UserRepository` initialized with the provided session.
    """
    return UserRepository(session)


UserRepo = Annotated[UserRepository, Depends(get_user_repository)]
"""
Annotated type for injecting a UserRepository dependency.

This annotation is used in FastAPI endpoints to automatically resolve and inject
a `UserRepository` instance using the `get_user_repository` dependency.

Type:
    Annotated[UserRepository, Depends(get_user_repository)]
"""
