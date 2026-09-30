from fastapi import status
from app.core.security import verify_password, get_password_hash


def test_password_hashing():
    raw_pass = "MySecretPass123!"
    hashed = get_password_hash(raw_pass)
    assert hashed != raw_pass
    assert verify_password(raw_pass, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False


def test_register_user_success(client):
    payload = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "password": "SecurePassword123!",
        "preferred_currency": "GBP"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "jane@example.com"
    assert data["user"]["preferred_currency"] == "GBP"


def test_register_duplicate_email(client, test_user):
    payload = {
        "name": "Another Name",
        "email": test_user.email,
        "password": "Password123!",
        "preferred_currency": "USD"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"].lower()


def test_login_success(client, test_user):
    payload = {
        "email": test_user.email,
        "password": "Password123!"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == test_user.email


def test_login_wrong_password(client, test_user):
    payload = {
        "email": test_user.email,
        "password": "WrongPassword!"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_me(client, auth_headers, test_user):
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user.email
    assert data["name"] == test_user.name


def test_get_current_user_unauthorized(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
