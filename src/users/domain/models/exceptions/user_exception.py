from shared.domain import BadRequestException


class UserNotFoundError(BadRequestException):
    """Exception raised when a user is not found."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message or "User not found."
        self.status_code = 404


class UserAlreadyExistsError(BadRequestException):
    """Exception raised when a user already exists."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message or "User already exists."
        self.status_code = 409
