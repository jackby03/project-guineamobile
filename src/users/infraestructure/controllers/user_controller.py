from fastapi import APIRouter, Depends, HTTPException, status

from src.shared.infrastructure.schemas.database import get_db

from ....users.application.user_service_provider import UserServiceProvider
from ..schemas.user_schema import UserSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=dict, status_code=status.HTTP_200_OK)
async def test():
    return {"message": "User service is running"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(data_user: UserSchema, db=Depends(get_db)):
    service = UserServiceProvider(db)
    user = await service.register_user(data_user)
    return user


@router.get("/{user_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, db=Depends(get_db)):
    service = UserServiceProvider(db)
    user = await service.get_user_by_id(user_id)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
