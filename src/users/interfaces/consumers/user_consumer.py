from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage

from shared.infrastructure.database import AsyncSessionFactory
from shared.infrastructure.messaging import RABBITMQ_URL
from users.infraestructure.models import UserCreateModel
from users.infraestructure.repositories import UserRepository

USER_COMMAND_EXCHANGE = "user_commands_exchange"
CREATE_USER_QUEUE = "create_user_queue"
CREATE_USER_ROUTING_KEY = "user.command.create"


async def process_create_user_message(message: AbstractIncomingMessage):
    """
    Asynchronously processes a message to create a new user.

    This function handles incoming messages containing user creation data. It decodes
    the message payload, validates it against the `UserCreateModel`, and persists the
    new user to the database.

    Args:
        message (AbstractIncomingMessage): The incoming message containing user creation data.
            The message body should be UTF-8 encoded JSON that matches the `UserCreateModel` schema.

    Raises:
        Exception: If any error occurs during message processing, decoding, validation,
            or database operations. The original exception is re-raised after logging.
    """
    async with message.process():
        try:
            # Decode the message body
            payload = message.body.decode("utf-8")
            user_data = UserCreateModel.model_validate_json(payload)

            print(f"Received message: {user_data}")

            # Save the user to the database
            async with AsyncSessionFactory() as session:
                user_repository = UserRepository(session)
                await user_repository.create_user(user_data)

            print(f"User {user_data.email} created successfully.")
        except Exception as e:
            print(f"Error processing message: {e}")
            raise


async def consume_create_user_commands():
    """
    Establishes a connection to RabbitMQ and sets up a consumer for user creation commands.

    This coroutine creates a robust connection to RabbitMQ, declares a direct exchange
    and queue for handling user creation commands, and starts consuming messages.
    The consumed messages are processed by the `process_create_user_message` callback.

    Returns:
        None

    Raises:
        aio_pika.exceptions.AMQPException: If connection or channel operations fail.
    """
    connection = await connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    # Declare the exchange and queue
    exchange = await channel.declare_exchange(USER_COMMAND_EXCHANGE, type="direct")
    queue = await channel.declare_queue(CREATE_USER_QUEUE, durable=True)
    await queue.bind(exchange, routing_key=CREATE_USER_ROUTING_KEY)

    print(f"Waiting for messages in {CREATE_USER_QUEUE}...")
    await queue.consume(process_create_user_message)
