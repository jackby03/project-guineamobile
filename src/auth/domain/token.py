from sqlalchemy import Column, String, Integer

from src.shared.infrastructure.database import Base


class Credential(Base):
    __tablename__ = "tb_tokens"

    credential_id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    access_token: str = Column(String, nullable=False)
    token_type: str = "bearer"
