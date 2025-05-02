# Base Exception for the application
class ApplicationError(Exception):
    """Base class for application-specific errors."""

    def __init__(self, message: str = "An unexpected error occurred."):
        self.message = message
        super().__init__(message)


# Domain Layer Errors
class DomainError(ApplicationError):
    """Base class for domain-related errors."""

    def __init__(self, message: str = "A domain error occurred."):
        super().__init__(message)


class EntityNotFoundError(DomainError):
    """Raise when an entity is not found."""

    def __init__(self, message: str = "Entity not found."):
        super().__init__(message)


# Application Layer Errors
class ApplicationServiceError(ApplicationError):
    """Base class for application service-related errors."""

    def __init__(self, message: str = "An application service error occurred."):
        super().__init__(message)


class AuthorizationError(ApplicationError):
    """Raise for authorization-related issues."""

    def __init__(self, message: str = "Action not authorized."):
        super().__init__(message)


# Infrastructure Layer Errors
class InfrastructureError(ApplicationError):
    """Base class for infrastructure-related errors."""

    def __init__(self, message: str = "An infrastructure error occurred."):
        super().__init__(message)


class MessagingError(InfrastructureError):
    """Raise for messaging queue-related issues."""

    def __init__(self, message: str = "A messaging error occurred."):
        super().__init__(message)
