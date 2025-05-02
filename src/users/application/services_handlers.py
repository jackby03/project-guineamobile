from shared.infrastructure.messaging import get_rabbitmq_channel
from src.shared.domain.helpers import exit_json
from src.users.application.use_cases.commands import RegisterUserUseCase
from src.users.application.use_cases.queries import GetUserByIdUseCase
from src.users.infraestructure.models import UserCreateModel, UserFindModel
from src.users.infraestructure.repositories import UserRepository
from users.infraestructure.messaging import UserCommandPublisher


class UserServiceHandler:
    """
    Handles user-related operations such as registration and retrieval by ID.

    This class serves as a service layer that interacts with the user repository and messaging system.
    It provides methods for registering a new user and retrieving user information by ID.
    """

    def __init__(self, db_session):
        """
        Initializes the UserServiceHandler with a database session.
        """
        self.user_repository = UserRepository(db_session)

    async def register_user(self, data_user: UserCreateModel):
        """
        Handles the registration of a new user in the system and publishes a user creation command.
        """
        try:
            use_case = RegisterUserUseCase(self.user_repository)
            user = await use_case.execute(data_user)

            if user is None:
                return exit_json(0, {"success": False, "message": "ERROR_REGISTER"})

            channel = await get_rabbitmq_channel()
            try:
                publisher = UserCommandPublisher(channel)
                await publisher.publish_create_user_command(data_user)
            finally:
                if channel and not channel.is_closed:
                    await channel.close()
                    print("RabbitMQ channel closed.")

            return exit_json(
                1,
                {
                    "success": True,
                    "message": "USER_REGISTERED",
                    "data": {
                        "user_id": user.user_id,
                        "name": user.name,
                        "email": user.email,
                    },
                },
            )
        except Exception as e:
            print("ERROR_REGISTRO", e)
            return exit_json(0, {"success": False, "message": str(e)})

    async def get_user_by_id(self, user_id: int):
        """
        Asynchronously retrieves a user by their ID.
        """
        try:
            use_case = GetUserByIdUseCase(self.user_repository)
            user = await use_case.execute(user_id)

            if user is None:
                return exit_json(0, {"message": "USUARIO_NO_ENCONTRADO"})

            user_map = UserFindModel(
                user_id=user.user_id, name=user.name, email=user.email
            )
            return exit_json(1, {"user": user_map})
        except Exception as e:
            print("ERROR_CONSULTA", e)
            return exit_json(0, {"message": str(e)})
