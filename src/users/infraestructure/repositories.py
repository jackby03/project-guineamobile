from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.domain.repositories import UserRepositoryInterface
from src.users.domain.user import User


class UserRepository(UserRepositoryInterface):
    """
    Implementation of the UserRepositoryInterface for interacting with the database.

    This class provides methods to retrieve and save user entities in the database
    using SQLAlchemy's asynchronous API.

    Attributes:
        db_session (AsyncSession): The SQLAlchemy asynchronous session used for database operations.
    """

    def __init__(self, db_session: AsyncSession):
        """
        Initializes the UserRepository with a database session.

        Args:
            db_session (AsyncSession): The SQLAlchemy asynchronous session used for database operations. :no-index:
        """
        self.db_session = db_session

    async def get_user_by_email(self, email: str) -> User:
        """
        Retrieves a user from the database by their email address.

        Args:
            email (str): The email address of the user to search for. :no-index:

        Returns:
            User: The user object if found, or `None` if no user exists with the given email.

        Raises:
            SQLAlchemyError: If there is an error executing the database query.
        """
        result = await self.db_session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        print(f"SQLAlchemy: Fetching user with email {email} from database.")
        return user

    async def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieves a user from the database by their ID.

        Args:
            user_id (int): The unique identifier of the user to retrieve. :no-index:

        Returns:
            User: The user object if found, or `None` if no user exists with the given ID.

        Raises:
            NoResultFound: If no user exists with the given ID and `scalar_one()` is used.
        """
        result = await self.db_session.execute(
            select(User).where(User.user_id == user_id)
        )
        user = result.scalar_one_or_none()
        print(f"SQLAlchemy: Fetching user with ID {user_id} from database.")
        return user

    async def save_user(self, user: User) -> User:
        """
        Saves a user entity to the database.
        """
        self.db_session.add(user)
        await self.db_session.commit()
        print(f"SQLAlchemy: User {user.user_id} saved to database.")
        return user
