from pydantic import BaseModel, EmailStr


class AuthenticateUserRequest(BaseModel):
    """
    A Pydantic model for user authentication requests.

    This class represents the structure of authentication requests,
    containing the necessary fields for user login.
    """

    username: EmailStr
    password: str


class TokenModel(BaseModel):
    """
    Data Transfer Object (DTO) for authentication tokens.

    This class represents the structure of authentication tokens in the application,
    containing the access token and its type.
    """

    access_token: str
    token_type: str

    class Config:
        from_attributes = True
