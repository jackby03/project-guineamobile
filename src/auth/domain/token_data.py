from pydantic import BaseModel


class TokenData(BaseModel):
    """Data extracted form validated token payload."""

    username: str | None = None
    user_id: str | None = None
