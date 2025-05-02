from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String

from shared.application.security import get_password_hash, verify_password
from src.shared.infrastructure.database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "tb_users"

    user_id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    hashed_password: str = Column(String, nullable=False)

    def set_password(self, password: str):
        self.hashed_password = get_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.hashed_password)

    def __repr__(self):
        return f"UserMode(id={self.user_id}, email='{self.email}', name='{self.name}')>"
