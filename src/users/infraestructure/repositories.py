from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.domain.repositories import UserRepositoryInterface
from src.users.domain.user import User


class UserRepository(UserRepositoryInterface):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_by_email(self, email: str) -> User:
        result = await self.db_session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        print(f"SQLAlchemy: Fetching user with email {email} from database.")
        return user

    async def get_user_by_id(self, user_id: int) -> User:
        result = await self.db_session.execute(
            select(User).where(User.user_id == user_id)
        )
        user = result.scalar_one_or_none()
        print(f"SQLAlchemy: Fetching user with ID {user_id} from database.")
        return user

    async def save_user(self, user: User) -> User:
        self.db_session.add(user)
        await self.db_session.commit()
        print(f"SQLAlchemy: User {user.user_id} saved to database.")
        return user
