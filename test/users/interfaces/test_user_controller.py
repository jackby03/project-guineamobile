from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.users.interfaces.user_controller import router

# filepath: e:\PycharmProjects\guinea\test\users\interfaces\test_user_controller.py

app = FastAPI()
app.include_router(router)


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "User service is running"}


@patch(
    "src.users.application.services_handlers.UserServiceHandler.register_user",
    new_callable=AsyncMock,
)
def test_register_user_success(mock_register_user, client):
    mock_register_user.return_value = {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com",
    }
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "securepassword123",
    }

    response = client.post("/register", json=user_data)
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com",
    }


@patch(
    "src.users.application.services_handlers.UserServiceHandler.register_user",
    new_callable=AsyncMock,
)
def test_register_user_failure(mock_register_user, client):
    mock_register_user.side_effect = Exception("Unexpected error")
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "securepassword123",
    }

    response = client.post("/register", json=user_data)
    assert response.status_code == 500
    assert response.json() == {
        "detail": "An error occurred while registering the user."
    }


@patch(
    "src.users.application.services_handlers.UserServiceHandler.get_user_by_id",
    new_callable=AsyncMock,
)
def test_get_user_by_id_success(mock_get_user_by_id, client):
    mock_get_user_by_id.return_value = {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com",
    }

    response = client.get("/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com",
    }


@patch(
    "src.users.application.services_handlers.UserServiceHandler.get_user_by_id",
    new_callable=AsyncMock,
)
def test_get_user_by_id_failure(mock_get_user_by_id, client):
    mock_get_user_by_id.side_effect = Exception("Unexpected error")

    response = client.get("/1")
    assert response.status_code == 500
    assert response.json() == {"detail": "An error occurred while retrieving the user."}
