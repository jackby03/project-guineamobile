from fastapi import APIRouter, HTTPException, status

from ....users.application.user_service_provider import UserServiceProvider

router = APIRouter(prefix="/users", tags=["users"])

service = UserServiceProvider()


@router.get("/", response_model=dict, status_code=status.HTTP_200_OK)
async def test():
    """
    Test endpoint to check if the service is running.
    Returns:
        A simple message indicating the service is running.
    """
    return {"message": "User service is running"}


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
