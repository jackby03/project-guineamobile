from auth.infrastructure.models import AuthenticateUserRequest
from shared.application.security import create_access_token
from shared.domain.base_errores import AuthorizationError
from users.infraestructure.repositories import UserRepository


class AuthenticateUserUseCase:
    """
    Use case for authenticating a user based on credentials.

    This class handles user authentication by validating credentials and generating access tokens.

    Attributes:
        user_repository (UserRepository): Repository for user-related database operations.

    Methods:
        execute(request: AuthenticateUserRequest) -> dict:
            Authenticates user credentials and generates an access token.

    Example:
        >>> use_case = AuthenticateUserUseCase(user_repository)
        >>> request = AuthenticateUserRequest(username="user@example.com", password="securepassword")
        >>> token = await use_case.execute(request)
        >>> print(token)
        {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", "token_type": "bearer"}
    """

    def __init__(self, user_repository: UserRepository):
        """
        Initializes the AuthenticateUserUseCase with a user repository.

        Args:
            user_repository (UserRepository): Repository for user-related database operations.
        """
        self.user_repository = user_repository

    async def execute(self, request: AuthenticateUserRequest) -> dict:
        """
        Authenticates the user and returns an access token upon success.

        This method validates the user's credentials by checking the email and password.
        If the credentials are valid, it generates a JWT access token.

        Args:
            request (AuthenticateUserRequest): The authentication request containing username and password.

        Returns:
            dict: Contains the access token and token type if authentication is successful.
                Format: {"access_token": str, "token_type": "bearer"}

        Raises:
            AuthorizationError: If the provided credentials are invalid.

        Example:
            >>> request = AuthenticateUserRequest(username="user@example.com", password="securepassword")
            >>> token = await use_case.execute(request)
            >>> print(token)
            {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", "token_type": "bearer"}
        """
        print(f"Authenticating user: {request.username}")

        user = await self.user_repository.get_user_by_email(request.username)
        if not user:
            raise AuthorizationError("Incorrect email or password.")

        if not user.verify_password(request.password):
            raise AuthorizationError("Incorrect email or password.")

        access_token_data = {"sub": str(user.user_id), "email": user.email}
        access_token = create_access_token(data=access_token_data)

        return {"access_token": access_token, "token_type": "bearer"}
