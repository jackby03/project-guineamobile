from pydantic import BaseModel


class TokenData(BaseModel):
    """A class representing token data for authentication purposes.
    This class inherits from Pydantic BaseModel and provides a structure for JWT token data.
    Attributes:
        username (str | None): The username associated with the token. Defaults to None.
        user_id (str | None): The unique identifier of the user. Defaults to None.
    """

    username: str | None = None
    user_id: str | None = None
