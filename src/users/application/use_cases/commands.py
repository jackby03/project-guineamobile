from src.users.domain.user import User
from src.users.domain.user_repository_interface import \
    UserRepositoryInterface
from src.users.infraestructure.user_schema import UserSchema


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def execute(self, command: UserSchema) -> User:
        new_user = User(name=command.name, email=command.email)
        saved_user = await self.user_repository.save_user(new_user)
        return saved_user
