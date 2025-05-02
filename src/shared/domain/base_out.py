from typing import Any, Optional

from pydantic import BaseModel


class Out:
    """
    Defines the output structure for use cases.

    This class represents a generic output structure that includes a state,
    a message, and an optional data payload.

    Attributes:
        state (int): The state of the operation (e.g., 0 for failure, 1 for success).
        msg (str): A message describing the result of the operation.
        data (dict): An optional dictionary containing additional data related to the operation.
    """

    def __init__(self, state: int, msg: str):
        """
        Initializes the Out object.

        Args:
            state (int): The state of the operation (e.g., 0 for failure, 1 for success).
            msg (str): A message describing the result of the operation.
        """
        self.state = state
        self.msg = msg
        self.data = {}


class BaseM(BaseModel):
    """
    Defines the output model for use cases.

    This Pydantic model is used to validate and serialize the output of use cases,
    ensuring a consistent structure for API responses.

    Attributes:
        state (int): The state of the operation (e.g., 0 for failure, 1 for success).
        msg (str): A message describing the result of the operation.
        data (Optional[Any]): An optional field containing additional data related to the operation.
    """

    state: int
    msg: str
    data: Optional[Any] = None
