from sqlalchemy import Column, Integer, String

from src.shared.infrastructure.database import Base


class User(Base):
    __tablename__ = "tb_users"

    user_id: int = Column(Integer,
                          primary_key=True,
                          index=True,
                          autoincrement=True)
    name: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    hashed_password: str = Column(String, nullable=False)

    def __repr__(self):
        return f"UserMode(id={self.user_id}, email='{self.email}', name='{self.name}')>"

