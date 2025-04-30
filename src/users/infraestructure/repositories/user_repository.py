from typing import Any, Type, Coroutine

from ...domain.models.entities.user import User
from ...domain.repositories.user_repository_interface import \
    UserRepositoryInterface

from ....shared.infrastructure.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository, UserRepositoryInterface):

    async def get_user_by_id(self, user_id: str) -> Coroutine[Any, Any, Type[User] | None]:
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
            user: User object containing user data.
        Returns:
            User object representing the created user.
        Raises:
            ValueError: If the user already exists or if there is an error
            during creation.
        """
        self.db_connection.add(user)
        self.db_connection.commit()
        return user
