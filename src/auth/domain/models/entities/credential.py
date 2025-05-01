from pydantic import UUID3
from sqlalchemy import Column, String

from src.shared.infrastructure.schemas.database import Base


class Credential(Base):
    __tablename__ = "tb_credentials"

    id: str = Column(UUID3, primary_key=True, autoincrement=True)
    username: str = Column(String, unique=True)
    password_hash: str = Column(String)

    def __repr__(self):
        return f"Credential(id={self.id}, username={self.username})"
