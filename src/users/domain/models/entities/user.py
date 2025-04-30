from dataclasses import dataclass


@dataclass
class User:
    id: str
    name: str
    email: str

    def __post_init__(self):
        if not self.id:
            raise ValueError("User ID cannot be empty.")
        if not self.name:
            raise ValueError("User name cannot be empty.")
        if not self.email:
            raise ValueError("User email cannot be empty.")
