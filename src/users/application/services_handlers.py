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
        self.user_repository = UserRepository(db_session)

    async def register_user(self, data_user: UserCreateModel):
        """
        Handles the registration of a new user in the system and publishes a user creation command.
        This method performs the following operations:
        1. Registers a new user using the RegisterUserUseCase
        2. Publishes a user creation command to RabbitMQ
        3. Returns appropriate response with user details or error message
        Args:
            data_user (UserCreateModel): The user data model containing registration information
        Returns:
            dict: A dictionary containing:
                - success (bool): True if registration was successful, False otherwise
                - message (str): Status message describing the result
                - data (dict, optional): User details if registration was successful, containing:
                    - user_id: The ID of the registered user
                    - name: The name of the registered user
                    - email: The email of the registered user
        Raises:
            Exception: Any exception that occurs during the registration process will be caught
                      and returned as an error response
        Note:
            The method ensures proper cleanup of RabbitMQ channel resources even if an error occurs
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
        Args:
            user_id (int): The unique identifier of the user to retrieve.
        Returns:
            dict: A JSON response containing:
                - On success (status 1): The user information mapped to UserFindModel
                - On failure (status 0): Error message indicating user not found or exception details
        Raises:
            Exception: Any exception that occurs during user retrieval is caught and returned
                      as an error message in the response.
        Example:
            Success response:
            {
                "status": 1,
                "data": {
                    "user": {
                        "user_id": 1,
                        "name": "John Doe",
                        "email": "john@example.com"
                    }
                }
            }
            Error response:
            {
                "status": 0,
                "data": {
                    "message": "USUARIO_NO_ENCONTRADO"
                }
            }
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
