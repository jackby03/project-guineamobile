from domain.models.entities import User
from domain.repositories import UserRepositoryInterface

from shared.infraestructure.repositories import BaseRepository


class UserRepository(BaseRepository, UserRepositoryInterface):

    async def get_user_by_id(self, user_id: str) -> User:
        """
        Get user by ID from the database.
        Args:
            user_id: User ID to search for.
        Returns:
            User object representing the found user.
        Raises:
            ValueError: If the user does not exist.
        """
        return self.db_connection.get(User, user_id)

    def create_user(self, user: User) -> User:
        """
        Create a new user in the database.
        Args:
            user_data: User object containing user data.
        Returns:
            User object representing the created user.
        Raises:
            ValueError: If the user already exists or if there is an error
            during creation.
        """
        self.db_session.add(user)
        self.db_session.commit()
        return user
