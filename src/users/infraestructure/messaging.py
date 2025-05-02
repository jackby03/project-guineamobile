from aio_pika import Message
from aio_pika.abc import AbstractRobustChannel

from src.users.infraestructure.models import UserCreateModel

USER_COMMAND_EXCHANGE = "user_commands_exchange"
CREATE_USER_ROUTING_KEY = "user.command.create"


class UserCommandPublisher:
    """
    Publishes user-related commands to RabbitMQ.

    This class is responsible for sending messages to the RabbitMQ exchange
    for user commands, specifically the command to create a new user.
    It uses the aio-pika library for asynchronous communication with RabbitMQ.

    Attributes:
        channel (AbstractRobustChannel): The RabbitMQ channel used for publishing messages.
    """

    def __init__(self, channel: AbstractRobustChannel):
        """
        Initializes the UserCommandPublisher.

        Args:
            channel (AbstractRobustChannel): The RabbitMQ channel used for publishing messages.
        """
        self.channel = channel

    async def publish_create_user_command(self, command: UserCreateModel):
        """
        Publishes a create user command message to RabbitMQ.

        This method takes a `UserCreateModel` command object, serializes it to JSON,
        and publishes it to RabbitMQ using the default exchange and specified routing key.
        The message is marked as persistent with delivery mode 2.

        Args:
            command (UserCreateModel): The user creation command model containing user details.

        Returns:
            None

        Raises:
            AMQPError: If there is an error publishing to RabbitMQ.
        """
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
