from domain.repositories.user_repository_interface import \
    UserRepositoryInterface

from shared.infraestructure.database import user_table
from shared.infraestructure.repositories import BaseRepository


class UserRepository(BaseRepository, UserRepositoryInterface):

    def get_user_by_id(self, user_id: str) -> dict:
        """
        Get user by ID from the database.
        Args:
            user_id: User ID to search for.
        Returns:
            Dictionary containing user data if found, else None.
        """
        query = user_table.select().where(user_table.c.id == user_id)
        result = self.db_connection.execute(query).fetchone()
        return dict(result) if result else None

    def create_user(self, user_data: dict) -> dict:
        """
        Create a new user in the database.
        Args:
            user_data: Dictionary containing user data.
        Returns:
            Dictionary containing the created user data.
        """
        query = user_table.insert().values(user_data)
        result = self.db_connection.execute(query)
        return {**user_data, "id": str(result.inserted_primary_key[0])}
