from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    email: str


class UserFindSchema(UserSchema):
    user_id: int
