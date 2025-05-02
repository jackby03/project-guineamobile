from auth.infrastructure.models import AuthenticateUserRequest
from shared.application.security import create_access_token
from shared.domain.base_errores import AuthorizationError
from users.infraestructure.repositories import UserRepository


class AuthenticateUserUseCase:
    """
    Use case for authenticating a user based on credentials.

    This class handles user authentication by validating credentials and generating access tokens.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Initializes the AuthenticateUserUseCase with a user repository.
        """
        self.user_repository = user_repository

    async def execute(self, request: AuthenticateUserRequest) -> dict:
        """
        Authenticates the user and returns an access token upon success.

        This method validates the user's credentials by checking the email and password.
        If the credentials are valid, it generates a JWT access token.
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
