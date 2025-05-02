from pydantic import BaseModel


class UserModel(BaseModel):
    name: str
    email: str
    password: str


class UserFindModel(UserModel):
    user_id: int


class UserCreateModel(UserModel):
    pass
