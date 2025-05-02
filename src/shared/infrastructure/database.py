from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from shared.configuration.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, pool_pre_ping=True)

AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models.

    This class serves as the base for all SQLAlchemy ORM models in the application.
    It provides metadata and other shared functionality for database models.
    """

    pass


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an `AsyncSession` for a request.

    This function is used as a dependency in FastAPI to provide a database session
    for each request. It ensures that the session is properly closed after the request.

    Yields:
        AsyncSession: The SQLAlchemy asynchronous session.

    Raises:
        Exception: If an error occurs during the session lifecycle.
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


@async_sessionmaker
async def db_session_manager() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a session outside FastAPI dependency injection.

    This function is useful for scenarios where a database session is needed
    outside the context of FastAPI's dependency injection system.

    Yields:
        AsyncSession: The SQLAlchemy asynchronous session.

    Raises:
        Exception: If an error occurs during the session lifecycle.
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()  # Commit on successful exit
        except Exception:
            await session.rollback()
        finally:
            await session.close()


async def init_db():
    """
    Initialize the database.

    This function initializes the database by creating tables if they don't exist.
    It is primarily used for development or testing purposes. In production, use
    Alembic migrations for database schema management.

    Raises:
        Exception: If the database connection or table creation fails.
    """
    print("Database connection initialized.")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Database connection successful.")
    except Exception as e:
        print(f"Database connection failed: {e}")


async def close_db():
    """
    Close the database engine connections.

    This function disposes of the database engine, closing all active connections.
    """
    await engine.dispose()
    print("Database connections closed.")
