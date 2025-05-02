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
    summary="Health check for the User Service",
    description="Returns a message indicating that the User Service is running.",
)
async def test():
    """
    Health check endpoint for the User Service.

    This endpoint is used to verify that the User Service is running and accessible.

    Returns:
        dict: A dictionary containing a message indicating the service status.

    Example:
        >>> response = await test()
        >>> print(response)
        {"message": "User service is running"}
    """
    return {"message": "User service is running"}


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Registers a new user in the system with the provided data.",
)
async def register_user(data_user: UserCreateModel, db=Depends(get_db_session)):
    """
    Registers a new user in the system.

    This endpoint handles user registration by validating the provided data and
    saving the user to the database.

    Args:
        data_user (UserCreateModel): The user data model containing registration details.
        db: The database session dependency.

    Returns:
        dict: A dictionary containing the registration response.

    Raises:
        HTTPException:
            - 400: If a domain error occurs during registration.
            - 500: If an unexpected error occurs during registration.

    Example:
        >>> data_user = UserCreateModel(name="John Doe", email="john@example.com", password="securepassword")
        >>> response = await register_user(data_user, db)
        >>> print(response)
        {"success": True, "message": "USER_REGISTERED", "data": {...}}
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
    description="Retrieves a user by their unique identifier.",
    responses={status.HTTP_404_NOT_FOUND: {"description": "User not found"}},
)
async def get_user_by_id(user_id: int, db=Depends(get_db_session)):
    """
    Retrieves a user by their unique identifier.

    This endpoint fetches a user from the database based on the provided user ID.

    Args:
        user_id (int): The unique identifier of the user to retrieve.
        db: The database session dependency.

    Returns:
        dict: A dictionary containing the user details.

    Raises:
        HTTPException:
            - 404: If the user is not found.
            - 500: If an unexpected error occurs during retrieval.

    Example:
        >>> user_id = 1
        >>> response = await get_user_by_id(user_id, db)
        >>> print(response)
        {"user_id": 1, "name": "John Doe", "email": "john@example.com"}
    """
    try:
        service = UserServiceHandler(db)
        user = await service.get_user_by_id(user_id)
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