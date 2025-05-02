from typing import Annotated

from fastapi import Depends

from shared.infrastructure.dependencies import DbSession
from users.infraestructure.repositories import UserRepository


def get_user_repository(session: DbSession) -> UserRepository:
    """
    Get a UserRepository instance with a database session.
    Args:
        session (DbSession): The database session to be used by the repository.
    Returns:
        UserRepository: A new instance of UserRepository initialized with the provided session.
    """

    return UserRepository(session)


UserRepo = Annotated[UserRepository, Depends(get_user_repository)]
