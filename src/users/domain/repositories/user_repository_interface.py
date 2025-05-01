from abc import ABCMeta, abstractmethod

from ...domain.models.entities.user import User


class UserRepositoryInterface(metaclass=ABCMeta):
    """
    Abstract repository interface for user data access in the domain layer.
    This interface defines the contract for user data operations.
    """

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User:
        """
        Get user by ID from the system.
        Args:
            user_id: Unique identifier of the user.
        Returns:
            Dictionary representing the found user.
        """
        pass

    @abstractmethod
    async def save_user(self, user: User) -> User:
        """
        Create a new user in the system.
        Args:
            user: Dictionary containing user data.
        Returns:
            Dictionary representing the created user.
        """
        pass
