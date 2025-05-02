from pydantic import BaseModel


class Token(BaseModel):
    """
    Represents a token model for authentication.
    This class extends BaseModel and defines the structure of an authentication token,
    including the access token and its type.
    Attributes:
        access_token (str): The authentication access token string.
        token_type (str): The type of token, defaults to "bearer".
    """

    access_token: str
    token_type: str = "bearer"
