from src.users.domain.repositories import UserRepositoryInterface
from src.users.domain.user import User
from src.users.infraestructure.models import UserModel


class RegisterUserUseCase:
    """
    Use case for registering a new user.

    This class handles the logic for creating a new user in the system. It ensures
    that no user with the same email already exists, hashes the user's password,
    and saves the user to the database.
    """

    def __init__(self, user_repository: UserRepositoryInterface):
        """
        Initializes the RegisterUserUseCase with a user repository.
        """
        self.user_repository = user_repository

    async def execute(self, command: UserModel) -> User:
        """
        Executes the user creation command.

        This method creates a new user after verifying that no user exists with the given email.
        The password is securely hashed before saving.
        """
        existing_user = await self.user_repository.get_user_by_email(command.email)
        if existing_user:
            raise ValueError("User with this email already exists.")

        new_user = User(name=command.name, email=command.email)
        new_user.set_password(command.password)
        saved_user = await self.user_repository.save_user(new_user)
        return saved_user
