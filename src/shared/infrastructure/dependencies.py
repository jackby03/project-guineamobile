from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.database import get_db_session
from src.shared.infrastructure.messaging import Channel, get_rabbitmq_channel

# Type hint for database session dependency
DbSession = Annotated[AsyncSession, Depends(get_db_session)]

# Type hint for RabbitMQ channel dependency
MqChannel = Annotated[Channel, Depends(get_rabbitmq_channel)]
