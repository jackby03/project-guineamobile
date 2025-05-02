from pydantic import BaseModel, EmailStr


class AuthenticateUserRequest(BaseModel):
    """A Pydantic model for user authentication requests.
    This class represents the structure of authentication requests,
    containing the necessary fields for user login.
    Attributes:
        username (EmailStr): The user's email address used as username
        password (str): The user's password for authentication
    """

    username: EmailStr
    password: str


class TokenModel(BaseModel):
    """
    Data Transfer Object (DTO) for authentication tokens.
    This class represents the structure of authentication tokens in the application,
    containing the access token and its type.
    Attributes:
        access_token (str): The JWT access token string
        token_type (str): The type of token (e.g., "bearer")
    Configuration:
        from_attributes (bool): Enables ORM model attribute parsing
    """

    access_token: str
    token_type: str

    class Config:
        from_attributes = True
