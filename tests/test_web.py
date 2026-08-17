"""Tests for the snekdo web frontend."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from snekdo.api import create_app
from snekdo.web import get_template_env, register_web_routes


@pytest.fixture
def client(tmp_path: Path):
    """Create a test client with a temporary storage file and a logged-in user."""
    storage_file = tmp_path / "todos.json"
    app = create_app(storage_path=str(storage_file))
    app.state.template_env = get_template_env()
    app.state.storage_path = str(storage_file)
    register_web_routes(app, storage_path=str(storage_file))
    test_client = TestClient(app)

    # Register and login a user so all protected routes have a token
    test_client.post(
        "/auth/register",
        data={"username": "testuser", "password": "password123"},
    )
    test_client.post(
        "/auth/login",
        data={"username": "testuser", "password": "password123"},
    )
    # Store the user_id on the app state for tests to use (get it from storage)
    from snekdo.storage import UserStorage
    user_storage = UserStorage(storage_path=str(tmp_path / "users.json"))
    user = user_storage.get("testuser")
    app.state.user_id = user.id

    return test_client


class TestRegistration:
    """Tests for the web registration flow."""

    def test_web_registration_sets_created_at(self, client):
        """Test that web registration records a non-empty created_at."""
        from snekdo.storage import UserStorage

        user_storage = UserStorage(storage_path=str(client.app.state.user_id and client.app.state.storage_path.replace("todos.json", "users.json")))  # noqa: E501
        user = user_storage.get("testuser")
        assert user is not None
        assert user.created_at != ""
        assert "T" in user.created_at


class TestListPage:
    """Tests for the todo list page."""

    def test_list_page_shows_heading(self, client):
        response = client.get("/todos")
        assert response.status_code == 200
        assert "Todos" in response.text

    def test_empty_list_shows_message(self, client):
        response = client.get("/todos")
        assert "No todos found" in response.text

    def test_list_page_redirects_root(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "Todos" in response.text


class TestAddPage:
    """Tests for the add todo page."""

    def test_add_form_rendered(self, client):
        response = client.get("/todos/add")
        assert response.status_code == 200
        assert "Add Todo" in response.text
        assert 'name="title"' in response.text

    def test_add_todo_success(self, client):
        response = client.post(
            "/todos/add",
            data={"title": "Buy milk", "description": "From the store"},
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert response.headers["location"] == "/todos"

    def test_add_todo_missing_title(self, client):
        response = client.post(
            "/todos/add",
            data={"title": "", "description": "test"},
        )
        assert response.status_code == 200
        assert "Title is required" in response.text


class TestShowPage:
    """Tests for the show todo page."""

    def test_show_todo(self, client):
        # Create a todo first
        storage_file = Path(client.app.state.storage_path)
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage
        storage = TodoStorage(storage_path=str(storage_file))
        todo = Todo(title="Test todo", user_id=client.app.state.user_id)
        storage.add(todo)

        response = client.get(f"/todos/{todo.id}")
        assert response.status_code == 200
        assert todo.title in response.text

    def test_show_nonexistent_todo(self, client):
        response = client.get("/todos/nonexistent-id")
        assert response.status_code == 404


class TestEditPage:
    """Tests for the edit todo page."""

    def test_edit_form_rendered(self, client):
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage
        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))
        todo = Todo(title="Original title", user_id=client.app.state.user_id)
        storage.add(todo)

        response = client.get(f"/todos/{todo.id}/edit")
        assert response.status_code == 200
        assert "Edit Todo" in response.text
        assert "Original title" in response.text

    def test_edit_todo_success(self, client):
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage
        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))
        todo = Todo(title="Original", description="Old desc", user_id=client.app.state.user_id)  # noqa: E501
        storage.add(todo)

        response = client.post(
            f"/todos/{todo.id}/edit",
            data={
                "title": "Updated",
                "description": "New desc",
                "due": "2026-12-31",
                "priority": "high",
            },
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert response.headers["location"] == "/todos"

    def test_edit_todo_missing_title(self, client):
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage
        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))
        todo = Todo(title="Original", user_id=client.app.state.user_id)
        storage.add(todo)

        response = client.post(
            f"/todos/{todo.id}/edit",
            data={"title": "", "description": "test"},
        )
        assert response.status_code == 200
        assert "Title is required" in response.text


class TestCompleteAction:
    """Tests for the complete todo action."""

    def test_complete_todo_htmx(self, client):
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage
        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))
        todo = Todo(title="Test todo", user_id=client.app.state.user_id)
        storage.add(todo)

        response = client.post(
            f"/todos/{todo.id}/complete",
            headers={"HX-Request": "true"},
        )
        assert response.status_code == 200
        assert "✓" in response.text

    def test_complete_todo_redirect(self, client):
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage
        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))
        todo = Todo(title="Test todo", user_id=client.app.state.user_id)
        storage.add(todo)

        response = client.post(
            f"/todos/{todo.id}/complete",
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert response.headers["location"] == "/todos"

    def test_complete_nonexistent_todo(self, client):
        response = client.post("/todos/nonexistent-id/complete")
        assert response.status_code == 404


class TestDeleteAction:
    """Tests for the delete todo action."""

    def test_delete_todo_htmx(self, client):
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage
        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))
        todo = Todo(title="Test todo", user_id=client.app.state.user_id)
        storage.add(todo)

        response = client.post(
            f"/todos/{todo.id}/delete",
            headers={"HX-Request": "true"},
        )
        assert response.status_code == 200
        assert "No todos found" in response.text

    def test_delete_todo_redirect(self, client):
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage
        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))
        todo = Todo(title="Test todo", user_id=client.app.state.user_id)
        storage.add(todo)

        response = client.post(
            f"/todos/{todo.id}/delete",
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert response.headers["location"] == "/todos"

    def test_delete_nonexistent_todo(self, client):
        response = client.post("/todos/nonexistent-id/delete")
        assert response.status_code == 404


class TestProfilePage:
    """Tests for the user profile page."""

    def test_profile_page_renders(self, client):
        """Test that the profile page renders with user info."""
        response = client.get("/profile")
        assert response.status_code == 200
        assert "Profile" in response.text
        assert "testuser" in response.text

    def test_profile_page_shows_user_info(self, client):
        """Test that the profile page displays user information."""
        response = client.get("/profile")
        assert response.status_code == 200
        assert "Username" in response.text
        assert "Display Name" in response.text
        assert "Email" in response.text
        assert "Created At" in response.text

    def test_profile_page_has_update_form(self, client):
        """Test that the profile page has an update form."""
        response = client.get("/profile")
        assert response.status_code == 200
        assert 'name="display_name"' in response.text
        assert 'name="email"' in response.text
        assert "Update Profile" in response.text

    def test_profile_page_has_password_form(self, client):
        """Test that the profile page has a password change form."""
        response = client.get("/profile")
        assert response.status_code == 200
        assert 'name="current_password"' in response.text
        assert 'name="new_password"' in response.text
        assert 'name="confirm_password"' in response.text
        assert "Change Password" in response.text

    def test_profile_page_redirects_unauthenticated(self):
        """Test that unauthenticated users are redirected to login."""
        from fastapi.testclient import TestClient

        from snekdo.api import create_app
        from snekdo.web import get_template_env, register_web_routes

        storage_file = "/tmp/test_profile_unauth.json"
        import os
        if os.path.exists(storage_file):
            os.remove(storage_file)
        app = create_app(storage_path=storage_file)
        app.state.template_env = get_template_env()
        register_web_routes(app, storage_path=storage_file)
        test_client = TestClient(app)
        response = test_client.get("/profile", follow_redirects=False)
        assert response.status_code == 302
        assert "login" in response.headers["location"].lower()


class TestProfileUpdate:
    """Tests for the profile update functionality."""

    def test_update_display_name(self, client):
        """Test updating the display name."""
        from snekdo.storage import UserStorage

        user_storage = UserStorage(
            storage_path=str(
                client.app.state.storage_path.replace("todos.json", "users.json")
            )
        )
        response = client.post(
            "/profile/update",
            data={"display_name": "New Name", "email": ""},
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert response.headers["location"] == "/profile"

        user = user_storage.get("testuser")
        assert user.display_name == "New Name"

    def test_update_email(self, client):
        """Test updating the email."""
        from snekdo.storage import UserStorage

        user_storage = UserStorage(
            storage_path=str(
                client.app.state.storage_path.replace("todos.json", "users.json")
            )
        )
        response = client.post(
            "/profile/update",
            data={"display_name": "", "email": "new@example.com"},
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert response.headers["location"] == "/profile"

        user = user_storage.get("testuser")
        assert user.email == "new@example.com"

    def test_update_both_fields(self, client):
        """Test updating both display name and email."""
        from snekdo.storage import UserStorage

        user_storage = UserStorage(
            storage_path=str(
                client.app.state.storage_path.replace("todos.json", "users.json")
            )
        )
        response = client.post(
            "/profile/update",
            data={"display_name": "New Name", "email": "new@example.com"},
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert response.headers["location"] == "/profile"

        user = user_storage.get("testuser")
        assert user.display_name == "New Name"
        assert user.email == "new@example.com"

    def test_update_invalid_email(self, client):
        """Test that invalid email format shows an error."""
        response = client.post(
            "/profile/update",
            data={"display_name": "", "email": "not-an-email"},
        )
        assert response.status_code == 200
        assert "Invalid email format" in response.text

    def test_update_htmx_partial(self, client):
        """Test that HTMX requests return partial content."""
        response = client.post(
            "/profile/update",
            data={"display_name": "HTMX Name", "email": ""},
            headers={"HX-Request": "true"},
        )
        assert response.status_code == 200
        assert "HTMX Name" in response.text

    def test_update_empty_email_clears(self, client):
        """Test that empty string clears the email field."""
        from snekdo.storage import UserStorage

        # First set an email
        user_storage = UserStorage(
            storage_path=str(
                client.app.state.storage_path.replace("todos.json", "users.json")
            )
        )
        user_storage.update_profile(
            client.app.state.user_id, email="old@example.com"
        )

        response = client.post(
            "/profile/update",
            data={"display_name": "", "email": ""},
            follow_redirects=False,
        )
        assert response.status_code == 302

        user = user_storage.get("testuser")
        assert user.email == ""


class TestPasswordChange:
    """Tests for the password change functionality."""

    def test_change_password_success(self, client):
        """Test that password change succeeds with valid data."""
        from snekdo.auth import verify_password
        from snekdo.storage import UserStorage

        user_storage = UserStorage(
            storage_path=str(
                client.app.state.storage_path.replace("todos.json", "users.json")
            )
        )
        user = user_storage.get("testuser")
        original_hash = user.password_hash

        response = client.post(
            "/profile/password",
            data={
                "current_password": "password123",
                "new_password": "newpass123",
                "confirm_password": "newpass123",
            },
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert response.headers["location"] == "/profile"

        user = user_storage.get("testuser")
        assert user.password_hash != original_hash
        assert verify_password("newpass123", user.password_hash)

    def test_change_password_wrong_current(self, client):
        """Test that wrong current password shows an error."""
        response = client.post(
            "/profile/password",
            data={
                "current_password": "wrongpass",
                "new_password": "newpass123",
                "confirm_password": "newpass123",
            },
        )
        assert response.status_code == 200
        assert "Current password is incorrect" in response.text

    def test_change_password_short_new(self, client):
        """Test that short new password shows an error."""
        response = client.post(
            "/profile/password",
            data={
                "current_password": "password123",
                "new_password": "short",
                "confirm_password": "short",
            },
        )
        assert response.status_code == 200
        assert "at least 8 characters" in response.text

    def test_change_password_mismatch(self, client):
        """Test that mismatched passwords show an error."""
        response = client.post(
            "/profile/password",
            data={
                "current_password": "password123",
                "new_password": "newpass123",
                "confirm_password": "different",
            },
        )
        assert response.status_code == 200
        assert "Passwords do not match" in response.text

    def test_change_password_htmx(self, client):
        """Test that HTMX password change returns partial content."""
        response = client.post(
            "/profile/password",
            data={
                "current_password": "password123",
                "new_password": "newpass123",
                "confirm_password": "newpass123",
            },
            headers={"HX-Request": "true"},
        )
        assert response.status_code == 200


class TestUserIdFilter:
    """Tests for the user_id filtering in the web UI."""

    def test_web_created_todo_visible_in_web_list(self, client):
        """Test that a web-created todo (with user_id) is visible in the web list."""
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage

        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))
        todo = Todo(title="Web todo", user_id=client.app.state.user_id)
        storage.add(todo)

        response = client.get("/todos")
        assert response.status_code == 200
        assert todo.title in response.text

    def test_web_created_todo_not_visible_to_other_user(self, client, tmp_path):
        """Test that a todo belonging to one user is not visible to another."""
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage, UserStorage

        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))

        # Create a todo for a different user
        other_user_id = "other-user-123"
        todo = Todo(title="Other user's todo", user_id=other_user_id)
        storage.add(todo)

        response = client.get("/todos")
        assert response.status_code == 200
        assert "Other user's todo" not in response.text

    def test_cli_created_todo_visible_in_cli_list(self, client, tmp_path):
        """Test that a CLI-created todo (without user_id) is visible in CLI list.

        The CLI list does not filter by user_id, so todos without user_id
        are still visible there.
        """
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage

        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))
        # Simulate CLI-created todo (no user_id)
        todo = Todo(title="CLI todo")
        storage.add(todo)

        # Verify the todo is in storage
        todos = storage.load()
        assert len(todos) == 1
        assert todos[0].title == "CLI todo"
        assert todos[0].user_id is None

    def test_web_list_filters_by_user_id(self, client):
        """Test that the web list only shows todos for the authenticated user."""
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage

        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))

        # Create todos for different users
        todo1 = Todo(title="User 1 todo", user_id=client.app.state.user_id)
        todo2 = Todo(title="Other user todo", user_id="other-user-456")
        storage.add(todo1)
        storage.add(todo2)

        response = client.get("/todos")
        assert response.status_code == 200
        assert "User 1 todo" in response.text
        assert "Other user todo" not in response.text

    def test_web_add_sets_user_id(self, client):
        """Test that the web add endpoint sets user_id on created todos."""
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage

        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))

        # Create a todo via the web form
        response = client.post(
            "/todos/add",
            data={"title": "Web added todo"},
            follow_redirects=False,
        )
        assert response.status_code == 302

        # Verify the todo has user_id set
        todos = storage.load()
        assert len(todos) == 1
        assert todos[0].user_id == client.app.state.user_id
        assert todos[0].title == "Web added todo"

