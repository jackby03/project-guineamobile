from abc import ABCMeta, abstractmethod

from ...domain.models.entities.user import User
from ...domain.models.use_cases.commands.create_user import CreateUserCommand


class UserCommandService(metaclass=ABCMeta):
    """
    Abstract service for handling user commands in the domain layer.
    Following Command pattern for write operations.
    """

    @abstractmethod
    async def create_user(self, command: CreateUserCommand) -> User:
        """
        Create a new user in the system.
        Args:
            command: Command object containing user data.
        Returns:
            User object representing the created user.
        """
        pass
