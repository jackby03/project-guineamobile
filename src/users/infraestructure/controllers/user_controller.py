from application import UserServiceImpl
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/users", tags=["users"])

service = UserServiceImpl()


@router.get("/{user_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: str):
    """
    Get user by ID.
    Args:
        user_id: User ID to search for.
    Returns:
        User object representing the found user.
    Raises:
        HTTPException: If the user does not exist.
    """
    user = await service.get_user_by_id(user_id)
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
