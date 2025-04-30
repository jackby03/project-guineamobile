import os
from typing import Optional

from sqlalchemy import (Column, Connection, Engine, MetaData, String, Table,
                        create_engine)
from sqlalchemy.exc import SQLAlchemyError

metadata = MetaData()

user_table = Table(
    "user",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("name", String(50), nullable=False),
    Column("email", String(100), nullable=False, unique=True),
)


def init_db_engine(db_uri: Optional[str] = None) -> Engine:
    """
    Initialize the database engine.
    Args:
        db_uri: Optional database URI. If not provided, uses DB_URI.
    Returns:
        SQLAlchemy Engine instance
    Raises:
        ValueError: If no database URI is provided or found in environment.
    """
    uri = db_uri or os.getenv("DB_URI")
    if not uri:
        raise ValueError("Database URI provide argument or DB_URI")
    db_engine = create_engine(uri)
    __create_tables_if_not_exists(db_engine)
    return db_engine


def db_connect(db_engine: Engine) -> Connection:
    """
    Create a new database connection.
    Args:
        db_engine: SQLAlchemy Engine instance
    Returns:
        SQLAlchemy Connection instance
    Raises:
        SQLAlchemyError: If connection fails
    """
    try:
        return db_engine.connect()
    except SQLAlchemyError as e:
        raise SQLAlchemyError(f"Failed to connect to database: {str(e)}")


def close_db_connection(connection: Connection) -> None:
    """
    Close the database connection safely.
    Args:
        connection: SQLAlchemy Connection instance to close
    """
    try:
        if connection and not connection.closed:
            connection.close()
    except SQLAlchemyError:
        pass


def __create_tables_if_not_exists(db_engine: Engine) -> None:
    """
    Create database tables if they don't exist.
    Args:
        db_engine: SQLAlchemy Engine instance
    Raises:
        SQLAlchemyError: If table creation fails
    """
    try:
        metadata.create_all(db_engine, checkfirst=True)
    except SQLAlchemyError as e:
        raise SQLAlchemyError(f"Failed to create tables: {str(e)}")
