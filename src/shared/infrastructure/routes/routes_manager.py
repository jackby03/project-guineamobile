from fastapi import FastAPI

from ....users.infraestructure.controllers import user_controller as user


class RoutesManager:
    def __init__(self, app: FastAPI):
        self.app = app

    def include_router(self):
        self.app.include_router(user.router)
