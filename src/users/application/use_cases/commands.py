from src.users.domain.repositories import UserRepositoryInterface
from src.users.domain.user import User
from src.users.infraestructure.models import UserModel


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def execute(self, command: UserModel) -> User:
        new_user = User(name=command.name, email=command.email)
        new_user.set_password(command.hashed_password)
        saved_user = await self.user_repository.save_user(new_user)
        return saved_user
