from typing import Any, Optional

from pydantic import BaseModel


class Out:
    """Defines the output of the use case."""

    def __init__(self, state, msg):
        self.state = state
        self.msg = msg
        self.data = {}


class BaseM(BaseModel):
    """Defines the output of the use case."""

    state: int
    msg: str
    data: Optional[Any] = None
