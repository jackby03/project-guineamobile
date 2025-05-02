import asyncio

import aio_pika.exceptions
from aio_pika.abc import AbstractRobustChannel, AbstractRobustConnection
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed
from typing_extensions import AsyncGenerator, Optional, TypeAlias

from shared.configuration.config import settings
from src.shared.domain.base_errores import MessagingError

RABBITMQ_URL = settings.RABBITMQ_URL

Channel: TypeAlias = AbstractRobustChannel

_connection: Optional[AbstractRobustConnection] = None


async def get_rabbitmq_connection() -> AbstractRobustConnection:
    """
    Gets or creates the global RabbitMQ connection.

    Returns:
        AbstractRobustConnection: The global RabbitMQ connection instance.

    Raises:
        MessagingError: If the connection cannot be established.
    """
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
    reraise=True,
)
async def connection_to_rabbitmq() -> AbstractRobustConnection:
    """
    Establishes a robust connection to RabbitMQ with retries.

    Returns:
        AbstractRobustConnection: The RabbitMQ connection instance.

    Raises:
        ConnectionError: If the connection fails after retries.
    """
    try:
        connection = await aio_pika.connect_robust(RABBITMQ_URL, timeout=10)
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
    """
    Callback for when the RabbitMQ connection is closed.

    Args:
        connection (AbstractRobustConnection): The RabbitMQ connection instance.
        exc (Optional[BaseException]): The exception that caused the closure, if any.
    """
    print(f"RabbitMQ connection closed: {exc}")
    global _connection
    _connection = None


def on_connection_reconnect(connection: AbstractRobustConnection):
    """
    Callback for when the RabbitMQ connection is reconnected.

    Args:
        connection (AbstractRobustConnection): The RabbitMQ connection instance.
    """
    print("RabbitMQ connection reconnected")


async def close_rabbitmq_connection():
    """
    Closes the global RabbitMQ connection if it exists.
    """
    global _connection
    if _connection and not _connection.is_closed:
        await _connection.close()
        _connection = None
        print("RabbitMQ connection closed.")


async def get_rabbitmq_channel() -> AsyncGenerator[Channel, None]:
    """
    Provides a RabbitMQ channel for a request.

    Yields:
        Channel: The RabbitMQ channel instance.

    Raises:
        MessagingError: If the channel cannot be created or used.
    """
    try:
        connection = await get_rabbitmq_connection()
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)
        print("RabbitMQ channel acquired.")
        return channel
    except Exception as e:
        print(f"Error obtaining RabbitMQ channel: {e}")
        raise MessagingError(f"Failed to get or use RabbitMQ channel: {e}")


async def declare_exchange(
    channel: Channel,
    exchange_name: str,
    exchange_type: str = "direct",
    durable: bool = True,
):
    """
    Declares an exchange in RabbitMQ.

    Args:
        channel (Channel): The RabbitMQ channel instance.
        exchange_name (str): The name of the exchange to declare.
        exchange_type (str, optional): The type of the exchange (e.g., "direct"). Defaults to "direct".
        durable (bool, optional): Whether the exchange should be durable. Defaults to True.
    """
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
    """
    Declares a queue in RabbitMQ.

    Args:
        channel (Channel): The RabbitMQ channel instance.
        queue_name (str): The name of the queue to declare.
        durable (bool, optional): Whether the queue should be durable. Defaults to True.
        arguments (Optional[dict], optional): Additional arguments for the queue. Defaults to None.
    """
    print(f"Declaring queue: {queue_name} (durable: {durable})")
    await channel.declare_queue(
        name=queue_name,
        durable=durable,
        arguments=arguments,
    )


async def bind_queue(
    channel: Channel, exchange_name: str, queue_name: str, routing_key: str = ""
):
    """
    Binds a queue to an exchange in RabbitMQ.

    Args:
        channel (Channel): The RabbitMQ channel instance.
        exchange_name (str): The name of the exchange.
        queue_name (str): The name of the queue.
        routing_key (str, optional): The routing key for the binding. Defaults to "".
    """
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
    """
    Publishes a message to an exchange in RabbitMQ.

    Args:
        channel (Channel): The RabbitMQ channel instance.
        exchange_name (str): The name of the exchange.
        routing_key (str): The routing key for the message.
        body (bytes): The message body.
        content_type (str, optional): The content type of the message. Defaults to "application/json".
        delivery_mode (aio_pika.DeliveryMode, optional): The delivery mode of the message. Defaults to PERSISTENT.
    """
    print(f"Publishing message to exchange '{exchange_name}' with key '{routing_key}'")
    message = aio_pika.Message(
        body=body,
        content_type=content_type,
        delivery_mode=delivery_mode,
    )
    exchange = await channel.get_exchange(exchange_name)
    await exchange.publish(message, routing_key=routing_key)
    print("Message published successfully.")
