from typing import Any, Optional

from pydantic import BaseModel


class Out:
    """
    Defines the output structure for use cases.

    This class represents a generic output structure that includes a state,
    a message, and an optional data payload.
    """

    def __init__(self, state: int, msg: str):
        """
        Initializes the Out object.
        """
        self.state = state
        self.msg = msg
        self.data = {}


class BaseM(BaseModel):
    """
    Defines the output model for use cases.

    This Pydantic model is used to validate and serialize the output of use cases,
    ensuring a consistent structure for API responses.
    """

    state: int
    msg: str
    data: Optional[Any] = None
