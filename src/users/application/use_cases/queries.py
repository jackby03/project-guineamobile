from src.users.domain.repositories import UserRepositoryInterface
from src.users.domain.user import User


class GetUserByIdUseCase:
    """
    Use case for retrieving a user by their unique identifier.

    This class handles the logic for fetching a user from the repository
    based on the provided user ID.

    Attributes:
        user_repository (UserRepositoryInterface): Repository for user-related database operations.
    """

    def __init__(self, user_repository: UserRepositoryInterface):
        """
        Initializes the GetUserByIdUseCase with a user repository.

        Args:
            user_repository (UserRepositoryInterface): The repository used for user-related database operations.
        """
        self.user_repository = user_repository

    async def execute(self, user_id: int) -> User:
        """
        Executes the get user by ID query.

        This method retrieves a user from the repository based on the provided user ID.

        Args:
            user_id (int): The unique identifier of the user to retrieve.

        Returns:
            User: The user object corresponding to the provided ID.

        Raises:
            UserNotFoundError: If no user is found with the provided ID.

        Example:
            user = await get_user_by_id_use_case.execute(user_id=1)
        """
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")
        return user
