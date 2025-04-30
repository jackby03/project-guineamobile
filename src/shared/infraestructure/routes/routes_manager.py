from fastapi import FastAPI


class RoutesManager:
    def __init__(self, app: FastAPI):
        self.app = app
