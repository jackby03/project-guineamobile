from unittest.mock import AsyncMock

import pytest

from src.users.application.use_cases.queries import GetUserByIdUseCase
from src.users.domain.user import User


@pytest.fixture
def mock_user_repository():
    return AsyncMock()


@pytest.fixture
def get_user_by_id_use_case(mock_user_repository):
    return GetUserByIdUseCase(user_repository=mock_user_repository)


@pytest.mark.asyncio
async def test_get_user_by_id_success(get_user_by_id_use_case, mock_user_repository):
    mock_user = User(
        user_id=1,
        name="Test User",
        email="test@example.com",
        hashed_password="hashedpassword",
    )
    mock_user_repository.get_user_by_id.return_value = mock_user

    result = await get_user_by_id_use_case.execute(user_id=1)

    assert result == mock_user
    mock_user_repository.get_user_by_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(get_user_by_id_use_case, mock_user_repository):
    mock_user_repository.get_user_by_id.return_value = None

    with pytest.raises(ValueError, match="User with ID 1 not found."):
        await get_user_by_id_use_case.execute(user_id=1)

    mock_user_repository.get_user_by_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_get_user_by_id_repository_error(
    get_user_by_id_use_case, mock_user_repository
):
    mock_user_repository.get_user_by_id.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        await get_user_by_id_use_case.execute(user_id=1)

    mock_user_repository.get_user_by_id.assert_called_once_with(1)
