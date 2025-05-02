from pydantic import BaseModel


class Token(BaseModel):
    """
    Represents a token model for authentication.

    This class extends Pydantic's `BaseModel` and defines the structure of an authentication token,
    including the access token and its type.

    Attributes:
        access_token (str): The authentication access token string.
        token_type (str): The type of token, defaults to "bearer".

    Example:
        >>> token = Token(access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", token_type="bearer")
        >>> print(token.access_token)
        eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    """

    access_token: str
    token_type: str = "bearer"
