import asyncio
import os

import aio_pika.exceptions
from aio_pika.abc import AbstractRobustChannel, AbstractRobustConnection
from dotenv import load_dotenv
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed
from typing_extensions import AsyncGenerator, Optional, TypeAlias

from src.shared.domain.base_errores import MessagingError

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URI")

Channel: TypeAlias = AbstractRobustChannel

_connection: Optional[AbstractRobustConnection] = None


async def get_rabbitmq_connection() -> AbstractRobustConnection:
    """Gets or creates the global RabbitMQ connection."""
    global _connection
    if _connection is None or _connection.is_closed:
        print("Attempting to create a new RabbitMQ connection.")
        _connection = await connection_to_rabbitmq()
        print("RabbitMQ connection established.")
    return _connection


@retry(
    stop=stop_after_attempt(5),
    wait=wait_fixed(2),
    retry=retry_if_exception_type(
        (ConnectionError, asyncio.TimeoutError, aio_pika.exceptions.AMQPConnectionError)
    ),
    reraise=True,  # Reraise the exception if all retries fail
)
async def connection_to_rabbitmq() -> AbstractRobustConnection:
    """Establishes a robust connection to RabbitMQ with retries."""
    try:
        connection = await aio_pika.connect_robust(
            RABBITMQ_URL, timeout=10  # Connection timeout in seconds
        )
        connection.close_callbacks(on_connection_close)
        connection.reconnect_callbacks(on_connection_reconnect)
        return connection
    except (
        ConnectionError,
        asyncio.TimeoutError,
        aio_pika.exceptions.AMQPConnectionError,
    ) as e:
        print(f"Failed to connect to RabbitMQ: {e}. Retrying...")
        raise


def on_connection_close(
    connection: AbstractRobustConnection, exc: Optional[BaseException]
):
    print(f"RabbitMQ connection closed: {exc}")
    global _connection
    _connection = None


def on_connection_reconnect(connection: AbstractRobustConnection):
    print("RabbitMQ connection reconnected")


async def close_rabbitmq_connection():
    """Closes the global RabbitMQ connection if it exists."""
    global _connection
    if _connection and not _connection.is_closed:
        await _connection.close()
        _connection = None
        print("RabbitMQ connection closed.")


async def get_rabbitmq_channel() -> AsyncGenerator[Channel, None]:
    """
    Dependency that provides a RabbitMQ channel for a request.
    Ensure the channel is closed afterward.
    """
    connection = await get_rabbitmq_connection()
    channel = None
    try:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)
        print("RabbitMQ channel acquired.")
        yield channel
    except Exception as e:
        print(f"Error obtaining/using RabbitMQ channel: {e}")
        raise MessagingError(f"Failed to get or use RabbitMQ channel: {e}")
    finally:
        if channel and not channel.is_closed:
            await channel.close()
            print("RabbitMQ channel closed.")


async def declare_exchange(
    channel: Channel,
    exchange_name: str,
    exchange_type: str = "direct",
    durable: bool = True,
):
    """Declares an exchange."""
    print(
        f"Declaring exchange: {exchange_name} (type: {exchange_type}, durable: {durable})"
    )
    await channel.declare_exchange(
        name=exchange_name, type=aio_pika.ExchangeType(exchange_type), durable=durable
    )


async def declare_queue(
    channel: Channel,
    queue_name: str,
    durable: bool = True,
    arguments: Optional[dict] = None,
):
    """Declares a queue."""
    print(f"Declaring queue: {queue_name} (durable: {durable})")
    await channel.declare_queue(
        name=queue_name,
        durable=durable,
        arguments=arguments,  # e.g., {'x-dead-letter-exchange': 'dlx_exchange'}
    )


async def bind_queue(
    channel: Channel, exchange_name: str, queue_name: str, routing_key: str = ""
):
    """Binds a queue to an exchange."""
    print(
        f"Binding queue '{queue_name}' to exchange '{exchange_name}' with key '{routing_key}'"
    )
    queue = await channel.get_queue(queue_name)
    await queue.bind(exchange=exchange_name, routing_key=routing_key)


async def publish_message(
    channel: Channel,
    exchange_name: str,
    routing_key: str,
    body: bytes,
    content_type: str = "application/json",
    delivery_mode: aio_pika.DeliveryMode = aio_pika.DeliveryMode.PERSISTENT,
):
    """Publishes a message to an exchange."""
    print(f"Publishing message to exchange '{exchange_name}' with key '{routing_key}'")
    message = aio_pika.Message(
        body=body,
        content_type=content_type,
        delivery_mode=delivery_mode,  # Make message persistent
    )
    exchange = await channel.get_exchange(exchange_name)
    await exchange.publish(message, routing_key=routing_key)
    print("Message published successfully.")


# Example of setting up exchanges/queues (call this during startup or consumer setup)
async def setup_messaging_infrastructure(channel: Channel):
    """Sets up necessary exchanges and queues. Should be idempotent."""
    # Example for User Commands
    user_command_exchange = "user_commands_exchange"
    create_user_queue = "create_user_queue"
    create_user_routing_key = "user.command.create"

    await declare_exchange(
        channel, user_command_exchange, exchange_type="direct", durable=True
    )
    await declare_queue(channel, create_user_queue, durable=True)
    await bind_queue(
        channel, user_command_exchange, create_user_queue, create_user_routing_key
    )

    # Add declarations for other exchanges/queues (e.g., for Auth context)

    print("Messaging infrastructure setup complete.")
