from typing import Annotated

from fastapi import Depends

from shared.infrastructure.dependencies import DbSession
from users.infraestructure.repositories import UserRepository


def get_user_repository(session: DbSession) -> UserRepository:
    """Dependency provider for UserRepository Implementation."""
    return UserRepository(session)


UserRepo = Annotated[UserRepository, Depends(get_user_repository)]
