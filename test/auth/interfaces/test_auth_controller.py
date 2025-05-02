from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from auth.interfaces.auth_controller import router
from auth.interfaces.dependencies import AuthenticateUser
from shared.domain.base_errores import AuthorizationError, EntityNotFoundError

# filepath: e:\PycharmProjects\guinea\test\auth\interfaces\test_auth_controller.py

app = FastAPI()
app.include_router(router)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_authenticate_use_case():
    return AsyncMock()


@patch("auth.interfaces.dependencies.AuthenticateUser", new_callable=AsyncMock)
def test_login_for_access_token_success(mock_authenticate_use_case, client):
    mock_authenticate_use_case.execute.return_value = {
        "access_token": "testtoken",
        "token_type": "bearer",
    }
    app.dependency_overrides[AuthenticateUser] = lambda: mock_authenticate_use_case

    form_data = {"username": "test@example.com", "password": "securepassword123"}

    response = client.post("/token", data=form_data)

    assert response.status_code == 200
    assert response.json() == {"access_token": "testtoken", "token_type": "bearer"}
    mock_authenticate_use_case.execute.assert_called_once()

    app.dependency_overrides = {}


@patch("auth.interfaces.auth_controller.AuthenticateUser", new_callable=AsyncMock)
def test_login_for_access_token_invalid_credentials(mock_authenticate_use_case, client):
    mock_authenticate_use_case.execute.side_effect = AuthorizationError(
        "Invalid credentials"
    )
    form_data = {"username": "test@example.com", "password": "wrongpassword"}

    response = client.post("/token", data=form_data)

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}
    mock_authenticate_use_case.execute.assert_called_once()


@patch("auth.interfaces.auth_controller.AuthenticateUser", new_callable=AsyncMock)
def test_login_for_access_token_user_not_found(mock_authenticate_use_case, client):
    mock_authenticate_use_case.execute.side_effect = EntityNotFoundError(
        "User not found"
    )
    form_data = {"username": "nonexistent@example.com", "password": "securepassword123"}

    response = client.post("/token", data=form_data)

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}
    mock_authenticate_use_case.execute.assert_called_once()


@patch("auth.interfaces.auth_controller.AuthenticateUser", new_callable=AsyncMock)
def test_login_for_access_token_internal_error(mock_authenticate_use_case, client):
    mock_authenticate_use_case.execute.side_effect = Exception("Unexpected error")
    form_data = {"username": "test@example.com", "password": "securepassword123"}

    response = client.post("/token", data=form_data)

    assert response.status_code == 500
    assert response.json() == {
        "detail": "An internal error occurred during authentication."
    }
    mock_authenticate_use_case.execute.assert_called_once()
