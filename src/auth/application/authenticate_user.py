from auth.infrastructure.models import AuthenticateUserRequest
from shared.application.security import create_access_token
from shared.domain.base_errores import AuthorizationError
from users.infraestructure.repositories import UserRepository


class AuthenticateUserUseCase:
    """Use case for authenticating a user based on credentials."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, request: AuthenticateUserRequest):
        """
        Authenticate the user and returns an access token upon success.
        Raises:
            EntityNotFoundError: If the user with the given email doesn't exist.
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
