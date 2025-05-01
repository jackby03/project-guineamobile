from typing import Any, Coroutine, Type

from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.models.entities.user import User
from ...domain.repositories.user_repository_interface import \
    UserRepositoryInterface


class UserRepository(UserRepositoryInterface):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_by_id(
        self, user_id: int
    ) -> Coroutine[Any, Any, Type[User] | None]:
        return self.db_session.get(User, user_id)

    async def save_user(self, user: User) -> User:
        self.db_session.add(user)
        await self.db_session.commit()
        return user
