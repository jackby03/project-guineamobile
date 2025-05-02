from typing import Any, Optional

from pydantic import BaseModel


class Out:
    def __init__(self, state, msg):
        self.state = state
        self.msg = msg
        self.data = {}


class BaseM(BaseModel):
    state: int
    msg: str
    data: Optional[Any] = None
