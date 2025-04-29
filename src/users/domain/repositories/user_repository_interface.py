from abc import (
    ABCMeta,
    abstractmethod,
)


class UserRepositoryInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> dict:
        """Get user by ID."""
        pass

    @abstractmethod
    def create_user(self, user_data: dict) -> dict:
        """Create a new user."""
        pass

    @abstractmethod
    def update_user(self, user_id: str, user_data: dict) -> dict:
        """Update an existing user."""
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> bool:
        """Delete a user."""
        pass
