from unittest.mock import AsyncMock

import pytest

from src.users.application.use_cases.commands import RegisterUserUseCase
from src.users.domain.user import User
from src.users.infraestructure.models import UserModel


@pytest.fixture
def mock_user_repository():
    return AsyncMock()


@pytest.fixture
def register_user_use_case(mock_user_repository):
    return RegisterUserUseCase(user_repository=mock_user_repository)


@pytest.mark.asyncio
async def test_register_user_success(register_user_use_case, mock_user_repository):
    user_model = UserModel(
        name="Test User", email="test@example.com", password="securepassword123"
    )
    mock_user_repository.get_user_by_email.return_value = None
    mock_user_repository.save_user.return_value = User(
        user_id=1,
        name="Test User",
        email="test@example.com",
        hashed_password="hashedpassword",
    )

    result = await register_user_use_case.execute(user_model)

    assert result.user_id == 1
    assert result.name == "Test User"
    assert result.email == "test@example.com"
    mock_user_repository.get_user_by_email.assert_called_once_with("test@example.com")
    mock_user_repository.save_user.assert_called_once()


@pytest.mark.asyncio
async def test_register_user_email_already_exists(
    register_user_use_case, mock_user_repository
):
    user_model = UserModel(
        name="Test User", email="test@example.com", password="securepassword123"
    )
    mock_user_repository.get_user_by_email.return_value = User(
        user_id=1,
        name="Existing User",
        email="test@example.com",
        hashed_password="hashedpassword",
    )

    with pytest.raises(ValueError, match="User with this email already exists."):
        await register_user_use_case.execute(user_model)

    mock_user_repository.get_user_by_email.assert_called_once_with("test@example.com")
    mock_user_repository.save_user.assert_not_called()


@pytest.mark.asyncio
async def test_register_user_repository_error(
    register_user_use_case, mock_user_repository
):
    user_model = UserModel(
        name="Test User", email="test@example.com", password="securepassword123"
    )
    mock_user_repository.get_user_by_email.return_value = None
    mock_user_repository.save_user.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        await register_user_use_case.execute(user_model)

    mock_user_repository.get_user_by_email.assert_called_once_with("test@example.com")
    mock_user_repository.save_user.assert_called_once()
