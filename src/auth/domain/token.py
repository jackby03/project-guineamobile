from pydantic import BaseModel


class Token(BaseModel):
    """
    Represents a token model for authentication.

    This class extends Pydantic's `BaseModel` and defines the structure of an authentication token,
    including the access token and its type.
    """

    access_token: str
    token_type: str = "bearer"
