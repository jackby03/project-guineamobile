from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.shared.infrastructure.schemas.database import Base


class User(Base):
    __tablename__ = "tb_users"

    user_id: int = Column(Integer,
                          primary_key=True,
                          index=True,
                          autoincrement=True)
    name: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False, unique=True)

    credential = relationship("Credential", back_populates="user")

    def __repr__(self):
        return f"User(user_id={self.user_id}, name={self.name})"
