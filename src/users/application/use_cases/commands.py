from src.users.domain.repositories import UserRepositoryInterface
from src.users.domain.user import User
from src.users.infraestructure.models import UserModel


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def execute(self, command: UserModel) -> User:
        """
        Execute the user creation command.
        This method creates a new user after verifying that no user exists with the given email.
        The password is securely hashed before saving.
        Args:
            command (UserModel): The user data model containing name, email and password
        Returns:
            User: The newly created and saved user entity
        Raises:
            ValueError: If a user with the provided email already exists
        Example:
            user = await create_user.execute(UserModel(
                name="John Doe",
                email="john@example.com",
                password="secret123"
            ))
        """

        existing_user = await self.user_repository.get_user_by_email(command.email)
        if existing_user:
            raise ValueError("User with this email already exists.")

        new_user = User(name=command.name, email=command.email)
        new_user.set_password(command.password)
        saved_user = await self.user_repository.save_user(new_user)
        return saved_user
