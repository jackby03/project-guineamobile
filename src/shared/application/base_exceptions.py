class BadRequestException(Exception):
    """Base class for all exceptions in the application."""

    def __init__(self, message: str) -> None:
        Exception().__init__(self)
        self.message = message or {}

    def to_dict(self) -> dict:
        """Convert exception to dictionary."""
        return {"error": self.message}
