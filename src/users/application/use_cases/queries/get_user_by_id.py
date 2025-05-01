from src.users.domain.models.entities.user import User
from src.users.domain.repositories.user_repository_interface import \
    UserRepositoryInterface


class GetUserByIdUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def execute(self, user_id: int) -> User:
        user = await self.user_repository.get_user_by_id(user_id)
        return user
