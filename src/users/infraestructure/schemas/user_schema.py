from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    name: str
    email: EmailStr


class UserFindSchema(BaseModel):
    id_user: str
