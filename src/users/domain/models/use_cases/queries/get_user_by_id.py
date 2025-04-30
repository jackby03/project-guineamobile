from dataclasses import dataclass


@dataclass
class GetUserByIdQuery:
    id: str
