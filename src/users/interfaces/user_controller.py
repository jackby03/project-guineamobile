from fastapi import APIRouter, Depends, HTTPException, status

from src.shared.domain.base_errores import DomainError, EntityNotFoundError
from src.shared.infrastructure.database import get_db_session
from src.users.application.services_handlers import UserServiceHandler
from src.users.infraestructure.models import UserCreateModel

router = APIRouter()


@router.get(
    "/",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def test():
    return {"message": "User service is running"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(data_user: UserCreateModel, db=Depends(get_db_session)):
    """
    Register a new user in the system.
    Args:
        data_user (UserCreateModel): User data model containing registration information.
        db (Session, optional): Database session. Defaults to Depends(get_db_session).
    Returns:
        dict: Response containing the registered user information.
    Raises:
        HTTPException: 400 Bad Request if domain validation fails.
        HTTPException: 500 Internal Server Error if an unexpected error occurs.
    """

    try:
        service = UserServiceHandler(db)
        response = await service.register_user(data_user)
        return response
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error registering user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while registering the user.",
        )


@router.get(
    "/{user_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Get user by ID",
    responses={status.HTTP_404_NOT_FOUND: {"description": "User not found"}},
)
async def get_user_by_id(user_id: int, db=Depends(get_db_session)):
    """
    Retrieve a user by their ID from the database.
    Args:
        user_id (int): The unique identifier of the user to retrieve.
        db (Session): Database session dependency.
    Returns:
        User: The user object if found.
    Raises:
        HTTPException:
            - 404 Not Found if user doesn't exist
            - 500 Internal Server Error if an unexpected error occurs
    """
    try:
        service = UserServiceHandler(db)
        user = await service.get_user_by_id(user_id)
        print(user)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"Error getting user by ID {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the user.",
        )
