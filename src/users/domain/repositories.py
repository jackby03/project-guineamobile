from abc import ABCMeta, abstractmethod

from src.users.domain.user import User


class UserRepositoryInterface(metaclass=ABCMeta):
    """
    Abstract repository interface for user data access in the domain layer.

    This interface defines the contract for user data operations, ensuring
    that any implementation adheres to the required methods for interacting
    with user data.
    """

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieve a user by their unique identifier.

        Args:
            user_id (int): Unique identifier of the user.

        Returns:
            User: The user object corresponding to the given ID.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User:
        """
        Retrieve a user by their email address.

        Args:
            email (str): The email address of the user.

        Returns:
            User: The user object corresponding to the given email.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    async def save_user(self, user: User) -> User:
        """
        Save a new user to the system.

        Args:
            user (User): The user object containing user data to be saved.

        Returns:
            User: The saved user object.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError
