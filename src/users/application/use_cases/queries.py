from src.users.domain.repositories import UserRepositoryInterface
from src.users.domain.user import User


class GetUserByIdUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def execute(self, user_id: int) -> User:
        """Execute the get user by id query.
        This method retrieves a user from the repository based on the provided user ID.
        Args:
            user_id (int): The unique identifier of the user to retrieve.
        Returns:
            User: The user object corresponding to the provided ID.
        Raises:
            UserNotFoundError: If no user is found with the provided ID.
        """

        user = await self.user_repository.get_user_by_id(user_id)
        return user
