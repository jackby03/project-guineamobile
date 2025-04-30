from abc import ABCMeta, abstractmethod

from domain.models.entities.user import User
from domain.models.use_cases.queries.get_user_by_id import GetUserByIdQuery


class UserQueryService(metaclass=ABCMeta):
    """
    Abstract service for handling user queries in the domain layer.
    Following Query pattern for read operations.
    """

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
