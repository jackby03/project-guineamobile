from pydantic import BaseModel


class TokenData(BaseModel):
    """
    A class representing token data for authentication purposes.

    This class inherits from Pydantic's `BaseModel` and provides a structure for JWT token data.
    """

    username: str | None = None
    user_id: str | None = None
