from fastapi import FastAPI

from src.auth.interfaces import auth_controller as auth
from src.users.interfaces import user_controller as user


class RoutesManager:
    """
    A class that manages the routing configuration for FastAPI application.
    This class is responsible for including different routers with their respective prefixes
    and tags into the main FastAPI application.
    Args:
        app (FastAPI): The FastAPI application instance to which routes will be added.
    Example:
        ```python
        app = FastAPI()
        routes_manager = RoutesManager(app)
        routes_manager.include_router()
        ```
    """

    def __init__(self, app: FastAPI):
        self.app = app

    def include_router(self):
        self.app.include_router(user.router, prefix="/users", tags=["users"])
        self.app.include_router(auth.router, prefix="/auth", tags=["authentication"])
