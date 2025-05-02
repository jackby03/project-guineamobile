import os
from typing import AsyncGenerator

from dotenv import load_dotenv
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
    """Base class for SQLAlchemy models."""

    pass


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an AsyncSession for a request.
    Ensures the session is closed afterward.
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
    """Provide a session outside FastAPI dependency injection."""
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
    Optionally create tables if they don't exist. (useful for dev/testing).
    """
    # In a production scenario, you'd typically use Alembic migrations.
    # This is a simplified setup.
    # async with engine.begin() as conn:
    #     # await conn.run_sync(Base.metadata.drop_all) # Use with caution!
    #     await conn.run_sync(Base.metadata.create_all)
    print("Database connection initialized.")
    # Check connection (optional)
    try:
        # flake8: noqa: F841
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Database connection successful.")
    except Exception as e:
        print(f"Database connection failed: {e}")


async def close_db():
    """Close the database engine connections."""
    await engine.dispose()
    print("Database connections closed.")
