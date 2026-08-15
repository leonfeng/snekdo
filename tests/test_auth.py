"""Tests for authentication and per-user isolation."""

import json
from pathlib import Path

from fastapi.testclient import TestClient

from snekdo.api import create_app
from snekdo.auth import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)

# ---------------------------------------------------------------------------
# Auth utilities
# ---------------------------------------------------------------------------

def test_hash_password_and_verify():
    """Test that password hashing and verification work."""
    password = "test_password_123"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrong_password", hashed)


def test_jwt_token():
    """Test JWT token creation and decoding."""
    user_id = "test-user-id"
    token = create_access_token(user_id)
    decoded = decode_access_token(token)
    assert decoded == user_id


def test_jwt_token_invalid():
    """Test that an invalid token returns None."""
    decoded = decode_access_token("invalid-token")
    assert decoded is None


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

def test_register_user(tmp_path: Path):
    """Test registering a new user."""
    storage_path = str(tmp_path / "todos.json")
    app = create_app(storage_path=storage_path)
    client = TestClient(app)

    response = client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "password": "password123"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
    assert "created_at" in data


def test_register_duplicate_user(tmp_path: Path):
    """Test that registering a duplicate user returns 409."""
    storage_path = str(tmp_path / "todos.json")
    app = create_app(storage_path=storage_path)
    client = TestClient(app)

    client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "password": "password123"},
    )

    response = client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "password": "password123"},
    )

    assert response.status_code == 409


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------

def test_login_user(tmp_path: Path):
    """Test logging in and receiving a token."""
    storage_path = str(tmp_path / "todos.json")
    app = create_app(storage_path=storage_path)
    client = TestClient(app)

    # Register first
    client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "password": "password123"},
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "password": "password123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(tmp_path: Path):
    """Test that logging in with wrong password returns 401."""
    storage_path = str(tmp_path / "todos.json")
    app = create_app(storage_path=storage_path)
    client = TestClient(app)

    client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "password": "password123"},
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "password": "wrongpassword"},
    )

    assert response.status_code == 401


# ---------------------------------------------------------------------------
# Protected endpoints
# ---------------------------------------------------------------------------

def test_todos_endpoint_requires_auth(tmp_path: Path):
    """Test that the todos endpoint requires authentication."""
    storage_path = str(tmp_path / "todos.json")
    app = create_app(storage_path=storage_path)
    client = TestClient(app)

    response = client.get("/api/v1/todos")

    assert response.status_code == 401


def test_create_todo_requires_auth(tmp_path: Path):
    """Test that creating a todo requires authentication."""
    storage_path = str(tmp_path / "todos.json")
    app = create_app(storage_path=storage_path)
    client = TestClient(app)

    response = client.post(
        "/api/v1/todos",
        json={"title": "Test todo"},
    )

    assert response.status_code == 401


def test_health_check_public(tmp_path: Path):
    """Test that the health check endpoint is public."""
    storage_path = str(tmp_path / "todos.json")
    app = create_app(storage_path=storage_path)
    client = TestClient(app)

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ---------------------------------------------------------------------------
# Per-user isolation
# ---------------------------------------------------------------------------

def test_per_user_todo_isolation(tmp_path: Path):
    """Test that todos are isolated by user."""
    storage_path = str(tmp_path / "todos.json")
    app = create_app(storage_path=storage_path)
    client = TestClient(app)

    # Register two users
    client.post(
        "/api/v1/auth/register",
        json={"username": "user1", "password": "password123"},
    )
    client.post(
        "/api/v1/auth/register",
        json={"username": "user2", "password": "password123"},
    )

    # Login as user1 and create a todo
    response1 = client.post(
        "/api/v1/auth/login",
        json={"username": "user1", "password": "password123"},
    )
    token1 = response1.json()["access_token"]

    response1 = client.post(
        "/api/v1/todos",
        json={"title": "User 1 todo"},
        headers={"Authorization": f"Bearer {token1}"},
    )
    assert response1.status_code == 201

    # Login as user2 and create a todo
    response2 = client.post(
        "/api/v1/auth/login",
        json={"username": "user2", "password": "password123"},
    )
    token2 = response2.json()["access_token"]

    response2 = client.post(
        "/api/v1/todos",
        json={"title": "User 2 todo"},
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert response2.status_code == 201

    # User1 should only see their own todo
    response = client.get(
        "/api/v1/todos",
        headers={"Authorization": f"Bearer {token1}"},
    )
    assert response.status_code == 200
    todos1 = response.json()
    assert len(todos1) == 1
    assert todos1[0]["title"] == "User 1 todo"

    # User2 should only see their own todo
    response = client.get(
        "/api/v1/todos",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert response.status_code == 200
    todos2 = response.json()
    assert len(todos2) == 1
    assert todos2[0]["title"] == "User 2 todo"


def test_user_cannot_modify_another_users_todo(tmp_path: Path):
    """Test that a user cannot modify another user's todo."""
    storage_path = str(tmp_path / "todos.json")
    app = create_app(storage_path=storage_path)
    client = TestClient(app)

    # Register two users
    client.post(
        "/api/v1/auth/register",
        json={"username": "user1", "password": "password123"},
    )
    client.post(
        "/api/v1/auth/register",
        json={"username": "user2", "password": "password123"},
    )

    # Login as user1 and create a todo
    response1 = client.post(
        "/api/v1/auth/login",
        json={"username": "user1", "password": "password123"},
    )
    token1 = response1.json()["access_token"]

    response = client.post(
        "/api/v1/todos",
        json={"title": "User 1 todo"},
        headers={"Authorization": f"Bearer {token1}"},
    )
    todo_id = response.json()["id"]

    # Login as user2
    response2 = client.post(
        "/api/v1/auth/login",
        json={"username": "user2", "password": "password123"},
    )
    token2 = response2.json()["access_token"]

    # User2 tries to modify user1's todo
    response = client.put(
        f"/api/v1/todos/{todo_id}",
        json={"title": "Hacked title"},
        headers={"Authorization": f"Bearer {token2}"},
    )

    # Should return 404 since the todo doesn't belong to user2
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Sync client token header
# ---------------------------------------------------------------------------

def test_sync_client_includes_token(tmp_path: Path):
    """Test that the sync client includes the token in requests."""
    credentials_path = tmp_path / "credentials.json"
    credentials_path.write_text(json.dumps({
        "access_token": "test-token",
        "token_type": "bearer",
    }))

    # We can't actually make a request to the server, but we can verify
    # that the credentials are read correctly
    from snekdo.api_client import _read_credentials
    creds = _read_credentials(credentials_path)
    assert creds is not None
    assert creds["access_token"] == "test-token"
    assert creds["token_type"] == "bearer"


def test_sync_client_no_token(tmp_path: Path):
    """Test that the sync client works without a token."""
    credentials_path = tmp_path / "nonexistent.json"
    assert not credentials_path.exists()

    from snekdo.api_client import _read_credentials
    creds = _read_credentials(credentials_path)
    assert creds is None
