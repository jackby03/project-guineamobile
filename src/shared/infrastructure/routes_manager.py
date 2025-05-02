from fastapi import FastAPI

from src.auth.interfaces import auth_controller as auth
from src.users.interfaces import user_controller as user


class RoutesManager:
    """
    A class that manages the routing configuration for a FastAPI application.

    This class is responsible for including different routers with their respective prefixes
    and tags into the main FastAPI application.
    """

    def __init__(self, app: FastAPI):
        """
        Initializes the RoutesManager with a FastAPI application instance.
        """
        self.app = app

    def include_router(self):
        """
        Includes routers into the FastAPI application.

        This method adds the user and authentication routers to the application
        with their respective prefixes and tags.
        """
        self.app.include_router(user.router, prefix="/users", tags=["users"])
        self.app.include_router(auth.router, prefix="/auth", tags=["authentication"])
