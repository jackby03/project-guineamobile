from pydantic import BaseModel, EmailStr


class AuthenticateUserRequest(BaseModel):
    """Request model for user authentication."""

    username: EmailStr
    password: str
