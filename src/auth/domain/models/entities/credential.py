from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.shared.infrastructure.schemas.database import Base


class Credential(Base):
    __tablename__ = "tb_credentials"

    credential_id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id: int = Column(Integer, ForeignKey("tb_users.user_id", ondelete="CASCADE"))
    username: str = Column(String, unique=True, nullable=False)
    password_hash: str = Column(String, nullable=False)

    user = relationship("User", back_populates="credential")

    def __repr__(self):
        return f"Credential(id={self.credential_id}, username={self.username})"
