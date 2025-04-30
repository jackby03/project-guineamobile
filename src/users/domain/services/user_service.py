from abc import ABCMeta, abstractmethod

from domain.models.entities.user import User
from domain.models.use_cases.commands.create_user import CreateUserCommand
from domain.models.use_cases.queries.get_user_by_id import GetUserByIdQuery
from services.user_command_service import UserCommandService
from services.user_query_service import UserQueryService


class UserService(UserCommandService, UserQueryService, metaclass=ABCMeta):
    """
    Interface for user management service.
    This service combines both command and query operations
    for user management.
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

    @abstractmethod
    async def get_user_by_id(self, query: GetUserByIdQuery) -> User:
        """
        Get user by ID from the system.
        Args:
            query: Query object containing user ID.
        Returns:
            User object representing the found user.
        """
        pass
