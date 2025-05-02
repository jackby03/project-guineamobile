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
    """Processes a message from the create_user_queue."""
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
    """Sets up the RabbitMQ consumer for the create_user_queue."""
    connection = await connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    # Declare the exchange and queue
    exchange = await channel.declare_exchange(USER_COMMAND_EXCHANGE, type="direct")
    queue = await channel.declare_queue(CREATE_USER_QUEUE, durable=True)
    await queue.bind(exchange, routing_key=CREATE_USER_ROUTING_KEY)

    print(f"Waiting for messages in {CREATE_USER_QUEUE}...")
    await queue.consume(process_create_user_message)
