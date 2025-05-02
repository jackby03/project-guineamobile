from fastapi import FastAPI

from src.auth.interfaces import auth_controller as auth
from src.users.interfaces import user_controller as user


class RoutesManager:
    def __init__(self, app: FastAPI):
        self.app = app

    def include_router(self):
        self.app.include_router(user.router, prefix="/users", tags=["users"])
        self.app.include_router(auth.router, prefix="/auth", tags=["authentication"])
