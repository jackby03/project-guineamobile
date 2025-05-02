from typing import Any, Coroutine, Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.users.domain.repositories import UserRepositoryInterface
from src.users.domain.user import User


class UserRepository(UserRepositoryInterface):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_by_id(
        self, user_id: int
    ) -> Coroutine[Any, Any, Type[User] | None]:
        print(f"SQLAlchemy: Fetching user with ID {user_id} from database.")
        return self.db_session.get(User, user_id)

    async def save_user(self, user: User) -> User:
        self.db_session.add(user)
        await self.db_session.commit()
        print(f"SQLAlchemy: User {user.user_id} saved to database.")
        return user
