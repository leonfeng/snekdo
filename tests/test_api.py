"""Tests for the FastAPI REST API."""

from pathlib import Path

from fastapi.testclient import TestClient

from snekdo.api import TodoCreate, create_app
from snekdo.storage import TodoStorage


def _make_todo(title: str = "Test todo", description: str = "A test todo", due: str = "2025-12-31", priority: str = "medium"):  # noqa: E501
    """Helper to create a Todo with a known ID."""
    from snekdo.models import Todo
    return Todo(
        id="test-id-123",
        title=title,
        description=description,
        due=due,
        completed=False,
        created_at="2024-01-01T00:00:00",
        priority=priority,
    )


def _register_and_login(client: TestClient, username: str | None = None, password: str = "password123") -> tuple[str, str]:  # noqa: E501
    """Register a user and log in, returning the access token and user ID."""
    if username is None:
        import time
        username = f"testuser_{int(time.time() * 1000)}"
    register_response = client.post(
        "/api/v1/auth/register",
        json={"username": username, "password": password},
    )
    register_response.raise_for_status()
    user_id = register_response.json()["id"]
    response = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    return response.json()["access_token"], user_id


def _auth_header(token: str) -> dict:
    """Return the Authorization header."""
    return {"Authorization": f"Bearer {token}"}


def test_health_check(tmp_path: Path):
    """Test the health check endpoint returns 200 with status ok."""
    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_list_todos_empty(tmp_path: Path):
    """Test listing todos when the store is empty returns an empty array."""
    storage_path = str(tmp_path / "todos.json")
    app = create_app(storage_path=storage_path)
    client = TestClient(app)

    token, _ = _register_and_login(client)
    response = client.get("/api/v1/todos", headers=_auth_header(token))

    assert response.status_code == 200
    assert response.json() == []


def test_list_todos_with_data(tmp_path: Path):
    """Test listing todos returns the stored todos."""
    storage = TodoStorage(storage_path=str(tmp_path / "todos.json"))
    todo = _make_todo()

    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    token, user_id = _register_and_login(client)
    todo.user_id = user_id
    storage.add(todo)

    response = client.get("/api/v1/todos", headers=_auth_header(token))

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == todo.id
    assert data[0]["title"] == todo.title


def test_show_todo(tmp_path: Path):
    """Test showing a single todo by ID."""
    storage = TodoStorage(storage_path=str(tmp_path / "todos.json"))
    todo = _make_todo()

    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    token, user_id = _register_and_login(client)
    todo.user_id = user_id
    storage.add(todo)

    response = client.get(f"/api/v1/todos/{todo.id}", headers=_auth_header(token))

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo.id
    assert data["title"] == todo.title


def test_show_todo_not_found(tmp_path: Path):
    """Test showing a non-existent todo returns 404."""
    app = create_app()
    client = TestClient(app)

    token, _ = _register_and_login(client)
    response = client.get("/api/v1/todos/non-existent-id", headers=_auth_header(token))

    assert response.status_code == 404


def test_add_todo(tmp_path: Path):
    """Test adding a new todo via the API."""
    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    token, _ = _register_and_login(client)
    response = client.post(
        "/api/v1/todos",
        json={"title": "New todo", "description": "A new todo item", "due": "2027-12-31", "priority": "high"},  # noqa: E501
        headers=_auth_header(token),
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New todo"
    assert data["description"] == "A new todo item"
    assert data["priority"] == "high"
    assert data["completed"] is False


def test_add_todo_missing_title(tmp_path: Path):
    """Test adding a todo without a title returns 422."""
    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    token, _ = _register_and_login(client)
    response = client.post(
        "/api/v1/todos",
        json={"title": "", "description": "A todo without title"},
        headers=_auth_header(token),
    )

    assert response.status_code == 422


def test_add_todo_invalid_due_date(tmp_path: Path):
    """Test adding a todo with an invalid due date returns 422."""
    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    token, _ = _register_and_login(client)
    response = client.post(
        "/api/v1/todos",
        json={"title": "New todo", "due": "not-a-date"},
        headers=_auth_header(token),
    )

    assert response.status_code == 422


def test_todo_create_valid_due_date_preserved():
    """Test that to_todo() preserves a valid future due date."""
    todo = TodoCreate(title="Test", due="2027-12-31").to_todo()
    assert todo.due == "2027-12-31"


def test_todo_create_empty_due_becomes_none():
    """Test that to_todo() normalizes an empty string due to None."""
    todo = TodoCreate(title="Test", due="").to_todo()
    assert todo.due is None


def test_todo_create_default_due_is_none():
    """Test that to_todo() defaults the due date to None."""
    todo = TodoCreate(title="Test").to_todo()
    assert todo.due is None


def test_todo_create_invalid_due_raises_value_error():
    """Test that to_todo() raises ValueError for an invalid due date format."""
    import pytest

    with pytest.raises(ValueError):
        TodoCreate(title="Test", due="not-a-date").to_todo()


def test_todo_create_past_due_raises_value_error():
    """Test that to_todo() raises ValueError for a past due date."""
    import pytest

    with pytest.raises(ValueError):
        TodoCreate(title="Test", due="2020-01-01").to_todo()


def test_add_todo_invalid_due_returns_422_via_to_todo(tmp_path: Path):
    """Test that add_todo returns 422 when to_todo() raises ValueError."""
    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    token, _ = _register_and_login(client)
    response = client.post(
        "/api/v1/todos",
        json={"title": "New todo", "due": "not-a-date"},
        headers=_auth_header(token),
    )

    assert response.status_code == 422


def test_complete_todo(tmp_path: Path):
    """Test completing a todo."""
    storage = TodoStorage(storage_path=str(tmp_path / "todos.json"))
    todo = _make_todo()

    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    token, user_id = _register_and_login(client)
    todo.user_id = user_id
    storage.add(todo)

    response = client.post(f"/api/v1/todos/{todo.id}/complete", headers=_auth_header(token))  # noqa: E501

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True


def test_complete_todo_not_found(tmp_path: Path):
    """Test completing a non-existent todo returns 404."""
    app = create_app()
    client = TestClient(app)

    token, _ = _register_and_login(client)
    response = client.post("/api/v1/todos/non-existent-id/complete", headers=_auth_header(token))  # noqa: E501

    assert response.status_code == 404


def test_modify_todo(tmp_path: Path):
    """Test modifying a todo."""
    storage = TodoStorage(storage_path=str(tmp_path / "todos.json"))
    todo = _make_todo()

    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    token, user_id = _register_and_login(client)
    todo.user_id = user_id
    storage.add(todo)

    response = client.put(
        f"/api/v1/todos/{todo.id}",
        json={"title": "Updated title", "description": "Updated description"},
        headers=_auth_header(token),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["description"] == "Updated description"


def test_modify_todo_not_found(tmp_path: Path):
    """Test modifying a non-existent todo returns 404."""
    app = create_app()
    client = TestClient(app)

    token, _ = _register_and_login(client)
    response = client.put(
        "/api/v1/todos/non-existent-id",
        json={"title": "Updated title"},
        headers=_auth_header(token),
    )

    assert response.status_code == 404


def test_delete_todo(tmp_path: Path):
    """Test deleting a todo."""
    storage = TodoStorage(storage_path=str(tmp_path / "todos.json"))
    todo = _make_todo()

    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    token, user_id = _register_and_login(client)
    todo.user_id = user_id
    storage.add(todo)

    response = client.delete(f"/api/v1/todos/{todo.id}", headers=_auth_header(token))

    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_delete_todo_not_found(tmp_path: Path):
    """Test deleting a non-existent todo returns 404."""
    app = create_app()
    client = TestClient(app)

    token, _ = _register_and_login(client)
    response = client.delete("/api/v1/todos/non-existent-id", headers=_auth_header(token))  # noqa: E501

    assert response.status_code == 404


def test_custom_storage_path(tmp_path: Path):
    """Test using a custom storage path."""
    custom_storage = tmp_path / "custom" / "todos.json"
    app = create_app(storage_path=str(custom_storage))
    client = TestClient(app)

    token, _ = _register_and_login(client)
    response = client.get("/api/v1/todos", headers=_auth_header(token))

    assert response.status_code == 200
    assert response.json() == []


# ---------------------------------------------------------------------------
# User profile endpoints
# ---------------------------------------------------------------------------

def test_get_profile(tmp_path: Path):
    """Test getting the current user's profile."""
    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    token, _ = _register_and_login(client, username="testuser")
    response = client.get("/api/v1/users/me", headers=_auth_header(token))

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
    assert "created_at" in data
    assert data["display_name"] == ""
    assert data["email"] == ""


def test_get_profile_unauthenticated(tmp_path: Path):
    """Test that getting profile requires authentication."""
    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    response = client.get("/api/v1/users/me")

    assert response.status_code == 401


def test_update_profile(tmp_path: Path):
    """Test updating the current user's profile."""
    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    token, _ = _register_and_login(client)
    response = client.put(
        "/api/v1/users/me",
        json={"display_name": "Test User", "email": "test@example.com"},
        headers=_auth_header(token),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["display_name"] == "Test User"
    assert data["email"] == "test@example.com"


def test_update_profile_partial(tmp_path: Path):
    """Test updating only the display name."""
    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    token, _ = _register_and_login(client)
    client.put(
        "/api/v1/users/me",
        json={"display_name": "Test User"},
        headers=_auth_header(token),
    )

    response = client.get("/api/v1/users/me", headers=_auth_header(token))
    assert response.status_code == 200
    data = response.json()
    assert data["display_name"] == "Test User"
    assert data["email"] == ""


def test_update_profile_unauthenticated(tmp_path: Path):
    """Test that updating profile requires authentication."""
    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    response = client.put(
        "/api/v1/users/me",
        json={"display_name": "Test User"},
    )

    assert response.status_code == 401


def test_change_password(tmp_path: Path):
    """Test changing the user's password."""
    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    token, _ = _register_and_login(client)
    response = client.put(
        "/api/v1/users/me/password",
        json={
            "current_password": "password123",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123",
        },
        headers=_auth_header(token),
    )

    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_change_password_unauthenticated(tmp_path: Path):
    """Test that changing password requires authentication."""
    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    response = client.put(
        "/api/v1/users/me/password",
        json={
            "current_password": "password123",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123",
        },
    )

    assert response.status_code == 401


def test_change_password_wrong_current(tmp_path: Path):
    """Test that changing password with wrong current password returns 401."""
    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    token, _ = _register_and_login(client)
    response = client.put(
        "/api/v1/users/me/password",
        json={
            "current_password": "wrongpassword",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123",
        },
        headers=_auth_header(token),
    )

    assert response.status_code == 401


def test_change_password_mismatch(tmp_path: Path):
    """Test that changing password with mismatched new password returns 422."""
    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    token, _ = _register_and_login(client)
    response = client.put(
        "/api/v1/users/me/password",
        json={
            "current_password": "password123",
            "new_password": "newpassword123",
            "confirm_password": "differentpassword",
        },
        headers=_auth_header(token),
    )

    assert response.status_code == 422


def test_profile_isolation(tmp_path: Path):
    """Test that a user can only modify their own profile."""
    app = create_app(storage_path=str(tmp_path / "todos.json"))
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

    # Login as user1 and update profile
    response1 = client.post(
        "/api/v1/auth/login",
        json={"username": "user1", "password": "password123"},
    )
    token1 = response1.json()["access_token"]

    client.put(
        "/api/v1/users/me",
        json={"display_name": "User One", "email": "user1@example.com"},
        headers=_auth_header(token1),
    )

    # Verify user1's profile is updated
    response = client.get("/api/v1/users/me", headers=_auth_header(token1))
    assert response.status_code == 200
    assert response.json()["display_name"] == "User One"

    # Login as user2 and try to update user1's profile (using user2's token)
    response2 = client.post(
        "/api/v1/auth/login",
        json={"username": "user2", "password": "password123"},
    )
    token2 = response2.json()["access_token"]

    # User2 tries to update their own profile (not user1's - /me always refers to own)
    response = client.put(
        "/api/v1/users/me",
        json={"display_name": "User Two"},
        headers=_auth_header(token2),
    )
    assert response.status_code == 200
    data = response.json()
    assert data["display_name"] == "User Two"

    # Verify user1's profile was not affected
    response = client.get("/api/v1/users/me", headers=_auth_header(token1))
    assert response.status_code == 200
    assert response.json()["display_name"] == "User One"


def test_delete_account_success(tmp_path: Path):
    """Test deleting an account with the correct password succeeds."""
    storage_path = str(tmp_path / "todos.json")
    app = create_app(storage_path=storage_path)
    client = TestClient(app)

    token, _ = _register_and_login(client)

    # Verify the user exists before deletion
    response = client.get("/api/v1/users/me", headers=_auth_header(token))
    assert response.status_code == 200

    # Delete the account
    response = client.request(
        "DELETE",
        "/api/v1/users/me",
        json={"password": "password123"},
        headers=_auth_header(token),
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "deleted" in data["message"].lower()

    # Verify the user no longer exists
    response = client.get("/api/v1/users/me", headers=_auth_header(token))
    assert response.status_code in (401, 403)


def test_delete_account_wrong_password(tmp_path: Path):
    """Test deleting an account with the wrong password returns 401."""
    storage_path = str(tmp_path / "todos.json")
    app = create_app(storage_path=storage_path)
    client = TestClient(app)

    token, _ = _register_and_login(client)

    response = client.request(
        "DELETE",
        "/api/v1/users/me",
        json={"password": "wrongpassword"},
        headers=_auth_header(token),
    )
    assert response.status_code == 401


def test_delete_account_missing_password(tmp_path: Path):
    """Test deleting an account without a password returns 422."""
    storage_path = str(tmp_path / "todos.json")
    app = create_app(storage_path=storage_path)
    client = TestClient(app)

    token, _ = _register_and_login(client)

    response = client.request(
        "DELETE",
        "/api/v1/users/me",
        json={"password": ""},
        headers=_auth_header(token),
    )
    assert response.status_code == 422


def test_delete_account_no_token(tmp_path: Path):
    """Test deleting an account without a token returns 401."""
    storage_path = str(tmp_path / "todos.json")
    app = create_app(storage_path=storage_path)
    client = TestClient(app)

    response = client.request(
        "DELETE",
        "/api/v1/users/me",
        json={"password": "password123"},
    )
    assert response.status_code == 401


def test_delete_account_cascades_to_todos(tmp_path: Path):
    """Test that deleting a user also deletes their todos."""
    storage_path = str(tmp_path / "todos.json")
    app = create_app(storage_path=storage_path)
    client = TestClient(app)

    token, user_id = _register_and_login(client)

    # Create a todo belonging to the user
    todo = _make_todo()
    todo.user_id = user_id
    storage = TodoStorage(storage_path=storage_path)
    storage.add(todo)

    # Delete the account
    response = client.request(
        "DELETE",
        "/api/v1/users/me",
        json={"password": "password123"},
        headers=_auth_header(token),
    )
    assert response.status_code == 200

    # Verify the todo is deleted
    todos = storage.get_all()
    assert len(todos) == 0


def _create_todo_for_user(storage_path: str, username: str, password: str = "password123"):  # noqa: E501
    """Register and login a user, create a todo for them, and return (token, todo_id)."""
    app = create_app(storage_path=storage_path)
    client = TestClient(app)
    token, user_id = _register_and_login(client, username=username, password=password)
    todo = _make_todo()
    todo.user_id = user_id
    TodoStorage(storage_path=storage_path).add(todo)
    return token, todo.id


def test_complete_cross_user_returns_404(tmp_path: Path):
    """Test that user B cannot complete user A's todo."""
    storage_path = str(tmp_path / "todos.json")
    token_a, todo_id = _create_todo_for_user(storage_path, "crossuser_a")

    # Register and login user B
    app = create_app(storage_path=storage_path)
    client = TestClient(app)
    token_b, _ = _register_and_login(client, username="crossuser_b")

    response = client.post(
        f"/api/v1/todos/{todo_id}/complete", headers=_auth_header(token_b)
    )

    assert response.status_code == 404


def test_modify_cross_user_returns_404(tmp_path: Path):
    """Test that user B cannot modify user A's todo."""
    storage_path = str(tmp_path / "todos.json")
    token_a, todo_id = _create_todo_for_user(storage_path, "crossuser_a")

    # Register and login user B
    app = create_app(storage_path=storage_path)
    client = TestClient(app)
    token_b, _ = _register_and_login(client, username="crossuser_b")

    response = client.put(
        f"/api/v1/todos/{todo_id}",
        json={"title": "Hacked title"},
        headers=_auth_header(token_b),
    )

    assert response.status_code == 404


def test_delete_cross_user_returns_404(tmp_path: Path):
    """Test that user B cannot delete user A's todo."""
    storage_path = str(tmp_path / "todos.json")
    token_a, todo_id = _create_todo_for_user(storage_path, "crossuser_a")

    # Register and login user B
    app = create_app(storage_path=storage_path)
    client = TestClient(app)
    token_b, _ = _register_and_login(client, username="crossuser_b")

    response = client.delete(
        f"/api/v1/todos/{todo_id}", headers=_auth_header(token_b)
    )

    assert response.status_code == 404


def test_create_todo_without_due_stores_none(tmp_path: Path):
    """Test that creating a todo without a due date stores None."""
    storage_path = str(tmp_path / "todos.json")
    app = create_app(storage_path=storage_path)
    client = TestClient(app)
    token, _ = _register_and_login(client)

    response = client.post(
        "/api/v1/todos",
        json={"title": "No due todo"},
        headers=_auth_header(token),
    )

    assert response.status_code == 201
    assert response.json()["due"] is None
    stored = TodoStorage(storage_path=storage_path).load()
    assert stored[0].due is None


def test_update_todo_completed_via_put(tmp_path: Path):
    """Test that updating the completed status via PUT works."""
    storage_path = str(tmp_path / "todos.json")
    app = create_app(storage_path=storage_path)
    client = TestClient(app)
    token, _ = _register_and_login(client)

    # Create a todo
    create_response = client.post(
        "/api/v1/todos",
        json={"title": "Test todo"},
        headers=_auth_header(token),
    )
    assert create_response.status_code == 201
    todo_id = create_response.json()["id"]

    # Update completed status
    response = client.put(
        f"/api/v1/todos/{todo_id}",
        json={"completed": True},
        headers=_auth_header(token),
    )

    assert response.status_code == 200
    assert response.json()["completed"] is True
    stored = TodoStorage(storage_path=storage_path).load()
    assert stored[0].completed is True


def test_update_todo_completed_false_via_put(tmp_path: Path):
    """Test that updating completed to false via PUT works."""
    storage_path = str(tmp_path / "todos.json")
    app = create_app(storage_path=storage_path)
    client = TestClient(app)
    token, _ = _register_and_login(client)

    # Create a todo
    create_response = client.post(
        "/api/v1/todos",
        json={"title": "Test todo"},
        headers=_auth_header(token),
    )
    assert create_response.status_code == 201
    todo_id = create_response.json()["id"]

    # Update completed status to false
    response = client.put(
        f"/api/v1/todos/{todo_id}",
        json={"completed": False},
        headers=_auth_header(token),
    )

    assert response.status_code == 200
    assert response.json()["completed"] is False


def test_update_todo_without_completed_does_not_error(tmp_path: Path):
    """Test that updating a todo without the completed field does not error."""
    storage_path = str(tmp_path / "todos.json")
    app = create_app(storage_path=storage_path)
    client = TestClient(app)
    token, _ = _register_and_login(client)

    # Create a todo
    create_response = client.post(
        "/api/v1/todos",
        json={"title": "Test todo"},
        headers=_auth_header(token),
    )
    assert create_response.status_code == 201
    todo_id = create_response.json()["id"]

    # Update only title
    response = client.put(
        f"/api/v1/todos/{todo_id}",
        json={"title": "Updated title"},
        headers=_auth_header(token),
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"
    assert response.json()["completed"] is False
