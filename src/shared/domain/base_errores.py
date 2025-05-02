# Base Exception for the application
class ApplicationError(Exception):
    """
    Base class for application-specific errors.

    This exception serves as the root for all custom exceptions in the application.
    """

    def __init__(self, message: str = "An unexpected error occurred."):
        """
        Initializes the ApplicationError.
        """
        self.message = message
        super().__init__(message)


# Domain Layer Errors
class DomainError(ApplicationError):
    """
    Base class for domain-related errors.

    This exception is raised for errors that occur in the domain layer of the application.
    """

    def __init__(self, message: str = "A domain error occurred."):
        """
        Initializes the DomainError.
        """
        super().__init__(message)


class EntityNotFoundError(DomainError):
    """
    Exception raised when an entity is not found.

    This exception is used to indicate that a requested entity does not exist in the system.
    """

    def __init__(self, message: str = "Entity not found."):
        """
        Initializes the EntityNotFoundError.
        """
        super().__init__(message)


# Application Layer Errors
class ApplicationServiceError(ApplicationError):
    """
    Base class for application service-related errors.

    This exception is raised for errors that occur in the application service layer.
    """

    def __init__(self, message: str = "An application service error occurred."):
        """
        Initializes the ApplicationServiceError.
        """
        super().__init__(message)


class AuthorizationError(ApplicationError):
    """
    Exception raised for authorization-related issues.

    This exception is used to indicate that an action is not authorized.
    """

    def __init__(self, message: str = "Action not authorized."):
        """
        Initializes the AuthorizationError.
        """
        super().__init__(message)


# Infrastructure Layer Errors
class InfrastructureError(ApplicationError):
    """
    Base class for infrastructure-related errors.

    This exception is raised for errors that occur in the infrastructure layer of the application.
    """

    def __init__(self, message: str = "An infrastructure error occurred."):
        """
        Initializes the InfrastructureError.
        """
        super().__init__(message)


class MessagingError(InfrastructureError):
    """
    Exception raised for messaging queue-related issues.

    This exception is used to indicate errors that occur in the messaging infrastructure.
    """

    def __init__(self, message: str = "A messaging error occurred."):
        """
        Initializes the MessagingError.
        """
        super().__init__(message)
