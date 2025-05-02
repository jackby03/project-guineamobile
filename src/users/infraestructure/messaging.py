from aio_pika import Message
from aio_pika.abc import AbstractRobustChannel

from src.users.infraestructure.models import UserCreateModel

USER_COMMAND_EXCHANGE = "user_commands_exchange"
CREATE_USER_ROUTING_KEY = "user.command.create"


class UserCommandPublisher:
    def __init__(self, channel: AbstractRobustChannel):
        self.channel = channel

    async def publish_create_user_command(self, command: UserCreateModel):
        """Publishes a CreateUserCommand."""
        message_body = command.model_dump_json().encode("utf-8")

        print(f"Publishing CreateUserCommand for email {command.email} to RabbitMQ.")
        await self.channel.default_exchange.publish(
            Message(
                body=message_body,
                content_type="application/json",
                delivery_mode=2,
            ),
            routing_key=CREATE_USER_ROUTING_KEY,
        )
        print("CreateUserCommand published successfully.")
