from shared.infrastructure.messaging import get_rabbitmq_channel
from src.shared.domain.helpers import exit_json
from src.users.application.use_cases.commands import RegisterUserUseCase
from src.users.application.use_cases.queries import GetUserByIdUseCase
from src.users.infraestructure.models import UserCreateModel, UserFindModel
from src.users.infraestructure.repositories import UserRepository
from users.infraestructure.messaging import UserCommandPublisher


class UserServiceHandler:
    def __init__(self, db_session):
        self.user_repository = UserRepository(db_session)

    async def register_user(self, data_user: UserCreateModel):
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
