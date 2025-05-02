from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String

from src.shared.infrastructure.database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "tb_users"

    user_id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    hashed_password: str = Column(String, nullable=False)

    def set_password(self, password: str):
        """Set the password for the user."""
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify the password for the user."""
        return pwd_context.verify(password, self.hashed_password)

    def __repr__(self):
        return f"UserMode(id={self.user_id}, email='{self.email}', name='{self.name}')>"
