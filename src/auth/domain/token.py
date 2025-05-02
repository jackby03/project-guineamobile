from pydantic import BaseModel


class Token(BaseModel):
    """Domain representation of a token."""

    access_token: str
    token_type: str = "bearer"
