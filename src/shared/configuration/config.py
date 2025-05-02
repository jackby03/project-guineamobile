from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings for the application.

    This class defines the configuration settings for the application, including
    application-level settings, database connection details, and RabbitMQ configuration.
    """

    # Application settings
    APP_NAME: str = "User Service"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "default_secret_key_change_me"
    ALGORITM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database settings
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/db_sample"

    # RabbitMQ settings
    RABBITMQ_URL: str = "amqp://guest:guest@localhost/"

    # Define model config to load from .env file
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Get the application settings.

    This function returns a cached instance of the `Settings` class, ensuring
    that the settings are loaded only once during the application's lifecycle.
    """
    return Settings()


# Global settings instance
settings = get_settings()
"""
Global instance of the application settings.

This instance provides access to all configuration settings defined in the `Settings` class.
"""
