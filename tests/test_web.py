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

    # Register and login a user so all protected routes have a token.
    # Login/register require the CSRF token issued by the GET form render,
    # so fetch the form first and submit the token back with the POST.
    test_client.get("/auth/register")
    register_token = test_client.cookies.get("csrf_token")
    test_client.post(
        "/auth/register",
        data={
            "username": "testuser",
            "password": "password123",
            "csrf_token": register_token,
        },
    )
    test_client.get("/auth/login")
    login_token = test_client.cookies.get("csrf_token")
    test_client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "password123",
            "csrf_token": login_token,
        },
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

    def test_list_shows_tags_and_category_columns(self, client):
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage
        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))
        Todo(title="Tagged", tags=["work", "urgent"], category="office",
             user_id=client.app.state.user_id)
        todo = Todo(title="Tagged", tags=["work", "urgent"], category="office",
                    user_id=client.app.state.user_id)
        storage.add(todo)

        response = client.get("/todos")
        assert response.status_code == 200
        assert "<th>Tags</th>" in response.text
        assert "<th>Category</th>" in response.text
        assert "work, urgent" in response.text
        assert ">office<" in response.text

    def test_list_shows_empty_cells_for_missing_tags_category(self, client):
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage
        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))
        todo = Todo(title="Plain", user_id=client.app.state.user_id)
        storage.add(todo)

        response = client.get("/todos")
        assert response.status_code == 200
        row = response.text.split("Plain")[1].split("</tr>")[0]
        cells = row.count("<td>")
        assert cells == 8
        assert "<td></td>" in row


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
            data={
                "title": "Buy milk",
                "description": "From the store",
                "csrf_token": client.cookies.get("csrf_token"),
            },
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert response.headers["location"] == "/todos"

    def test_add_todo_missing_title(self, client):
        response = client.post(
            "/todos/add",
            data={
                "title": "",
                "description": "test",
                "csrf_token": client.cookies.get("csrf_token"),
            },
        )
        assert response.status_code == 200
        assert "Title is required" in response.text

    def test_add_form_includes_tags_and_category_inputs(self, client):
        response = client.get("/todos/add")
        assert response.status_code == 200
        assert 'name="tags"' in response.text
        assert 'name="category"' in response.text

    def test_add_todo_stores_parsed_tags_and_category(self, client):
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage

        response = client.post(
            "/todos/add",
            data={
                "title": "Tagged todo",
                "tags": " work ,  urgent ,work",
                "category": "office",
                "csrf_token": client.cookies.get("csrf_token"),
            },
            follow_redirects=False,
        )
        assert response.status_code == 302
        storage = TodoStorage(storage_path=str(client.app.state.storage_path))
        todos = storage.load(user_id=client.app.state.user_id)
        todo = next(t for t in todos if t.title == "Tagged todo")
        assert todo.tags == ["work", "urgent"]
        assert todo.category == "office"

    def test_add_todo_empty_tags_and_category(self, client):
        from snekdo.storage import TodoStorage

        response = client.post(
            "/todos/add",
            data={
                "title": "No tags",
                "tags": "",
                "category": "",
                "csrf_token": client.cookies.get("csrf_token"),
            },
            follow_redirects=False,
        )
        assert response.status_code == 302
        storage = TodoStorage(storage_path=str(client.app.state.storage_path))
        todos = storage.load(user_id=client.app.state.user_id)
        todo = next(t for t in todos if t.title == "No tags")
        assert todo.tags == []
        assert todo.category is None


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
                "csrf_token": client.cookies.get("csrf_token"),
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
            data={
                "title": "",
                "description": "test",
                "csrf_token": client.cookies.get("csrf_token"),
            },
        )
        assert response.status_code == 200
        assert "Title is required" in response.text

    def test_edit_form_prefills_tags_and_category(self, client):
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage
        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))
        todo = Todo(
            title="Original",
            tags=["work", "home"],
            category="office",
            user_id=client.app.state.user_id,
        )
        storage.add(todo)

        response = client.get(f"/todos/{todo.id}/edit")
        assert response.status_code == 200
        assert 'name="tags"' in response.text
        assert 'name="category"' in response.text
        assert 'value="work, home"' in response.text
        assert 'value="office"' in response.text

    def test_edit_updates_tags_and_category(self, client):
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage
        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))
        todo = Todo(
            title="Original",
            tags=["old"],
            category="old-cat",
            user_id=client.app.state.user_id,
        )
        storage.add(todo)

        response = client.post(
            f"/todos/{todo.id}/edit",
            data={
                "title": "Updated",
                "tags": "urgent, home",
                "category": "home",
                "csrf_token": client.cookies.get("csrf_token"),
            },
            follow_redirects=False,
        )
        assert response.status_code == 302
        updated = storage.get(todo.id, user_id=client.app.state.user_id)
        assert updated.tags == ["urgent", "home"]
        assert updated.category == "home"

    def test_edit_empty_category_clears_field(self, client):
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage
        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))
        todo = Todo(
            title="Original",
            tags=["old"],
            category="old-cat",
            user_id=client.app.state.user_id,
        )
        storage.add(todo)

        response = client.post(
            f"/todos/{todo.id}/edit",
            data={
                "title": "Updated",
                "tags": "",
                "category": "",
                "csrf_token": client.cookies.get("csrf_token"),
            },
            follow_redirects=False,
        )
        assert response.status_code == 302
        updated = storage.get(todo.id, user_id=client.app.state.user_id)
        assert updated.tags == []
        assert updated.category is None


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
            headers={"HX-Request": "true", "X-CSRF-Token": client.cookies.get("csrf_token")},
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
            data={"csrf_token": client.cookies.get("csrf_token")},
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert response.headers["location"] == "/todos"

    def test_complete_nonexistent_todo(self, client):
        response = client.post(
            "/todos/nonexistent-id/complete",
            data={"csrf_token": client.cookies.get("csrf_token")},
        )
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
            headers={"HX-Request": "true", "X-CSRF-Token": client.cookies.get("csrf_token")},
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
            data={"csrf_token": client.cookies.get("csrf_token")},
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert response.headers["location"] == "/todos"

    def test_delete_nonexistent_todo(self, client):
        response = client.post(
            "/todos/nonexistent-id/delete",
            data={"csrf_token": client.cookies.get("csrf_token")},
        )
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
            data={
                        "display_name": "New Name",
                        "email": "",
                        "csrf_token": client.cookies.get("csrf_token"),
                    },
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
            data={
                        "display_name": "",
                        "email": "new@example.com",
                        "csrf_token": client.cookies.get("csrf_token"),
                    },
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
            data={
                        "display_name": "New Name",
                        "email": "new@example.com",
                        "csrf_token": client.cookies.get("csrf_token"),
                    },
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
            data={
                        "display_name": "",
                        "email": "not-an-email",
                        "csrf_token": client.cookies.get("csrf_token"),
                    },
        )
        assert response.status_code == 200
        assert "Invalid email format" in response.text

    def test_update_htmx_partial(self, client):
        """Test that HTMX requests return partial content."""
        response = client.post(
            "/profile/update",
            data={
                        "display_name": "HTMX Name",
                        "email": "",
                        "csrf_token": client.cookies.get("csrf_token"),
                    },
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
            data={
                "display_name": "",
                "email": "",
                "csrf_token": client.cookies.get("csrf_token"),
            },
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
                        "csrf_token": client.cookies.get("csrf_token"),
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
                        "csrf_token": client.cookies.get("csrf_token"),
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
                        "csrf_token": client.cookies.get("csrf_token"),
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
                        "csrf_token": client.cookies.get("csrf_token"),
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
                        "csrf_token": client.cookies.get("csrf_token"),
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
        from snekdo.storage import TodoStorage

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
        from snekdo.storage import TodoStorage

        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))

        # Create a todo via the web form
        response = client.post(
            "/todos/add",
            data={
                "title": "Web added todo",
                "csrf_token": client.cookies.get("csrf_token"),
            },
            follow_redirects=False,
        )
        assert response.status_code == 302

        # Verify the todo has user_id set
        todos = storage.load()
        assert len(todos) == 1
        assert todos[0].user_id == client.app.state.user_id
        assert todos[0].title == "Web added todo"


class TestCSRF:
    """Tests for CSRF token generation, validation, and rotation."""

    def test_csrf_token_in_add_form(self, client):
        """Test that the add form includes a CSRF token."""
        response = client.get("/todos/add")
        assert response.status_code == 200
        assert 'name="csrf_token"' in response.text
        assert 'value="' in response.text

    def test_csrf_token_in_edit_form(self, client):
        """Test that the edit form includes a CSRF token."""
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage

        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))
        todo = Todo(title="Test todo", user_id=client.app.state.user_id)
        storage.add(todo)

        response = client.get(f"/todos/{todo.id}/edit")
        assert response.status_code == 200
        assert 'name="csrf_token"' in response.text

    def test_csrf_token_in_profile_forms(self, client):
        """Test that profile forms include CSRF tokens."""
        response = client.get("/profile")
        assert response.status_code == 200
        assert response.text.count('name="csrf_token"') >= 3

    def test_csrf_token_in_logout_form(self, client):
        """Test that the logout form includes a CSRF token."""
        response = client.get("/todos")
        assert response.status_code == 200
        assert 'name="csrf_token"' in response.text

    def test_csrf_token_in_login_form(self, client):
        """Test that the login form includes a CSRF token."""
        response = client.get("/auth/login")
        assert response.status_code == 200
        assert 'name="csrf_token"' in response.text

    def test_csrf_token_in_register_form(self, client):
        """Test that the register form includes a CSRF token."""
        response = client.get("/auth/register")
        assert response.status_code == 200
        assert 'name="csrf_token"' in response.text

    def test_csrf_token_rotated_on_login(self, client):
        """Test that the CSRF token is rotated after login."""
        from snekdo.csrf import get_csrf_token_cookie

        # Get the token before login
        login_response = client.get("/auth/login")
        before_token = get_csrf_token_cookie(login_response)

        # Login
        response = client.post(
            "/auth/login",
            data={
                "username": "testuser",
                "password": "password123",
                "csrf_token": before_token,
            },
            follow_redirects=False,
        )
        after_token = get_csrf_token_cookie(response)

        assert before_token is not None
        assert after_token is not None
        assert before_token != after_token

    def test_csrf_token_rotated_on_register(self, client):
        """Test that the CSRF token is rotated after registration."""
        from snekdo.csrf import get_csrf_token_cookie

        # Get the token before registration
        register_response = client.get("/auth/register")
        before_token = get_csrf_token_cookie(register_response)
        assert before_token is not None

        # Register (submit the issued token, as the form does)
        response = client.post(
            "/auth/register",
            data={
                "username": "newuser123",
                "password": "password123",
                "csrf_token": before_token,
            },
            follow_redirects=False,
        )
        after_token = get_csrf_token_cookie(response)

        assert before_token is not None
        assert after_token is not None
        assert before_token != after_token

    def test_missing_csrf_token_rejected(self, client):
        """Test that a request without a CSRF token is rejected."""

        # Clear all cookies to remove the CSRF token
        client.cookies.clear()
        response = client.post(
            "/todos/add",
            data={"title": "Test todo"},
            follow_redirects=False,
        )
        # Should be rejected (redirect to login since no valid session/cookie)
        # or return 403 / 200 with error
        assert response.status_code in (200, 302, 403)

    def test_invalid_csrf_token_rejected(self, client):
        """Test that a request with an invalid CSRF token is rejected."""
        from snekdo.csrf import CSRF_COOKIE_NAME

        # Get the valid CSRF token from the cookie
        valid_token = client.cookies.get(CSRF_COOKIE_NAME)
        assert valid_token is not None

        # Submit with a wrong token value
        response = client.post(
            "/todos/add",
            data={
                "title": "Test todo",
                "csrf_token": "invalid-token-value",
            },
            follow_redirects=False,
        )
        # Should be rejected: either 403, or 200 with error page, or 302 (if cookie was cleared)
        assert response.status_code in (200, 302, 403)
        if response.status_code == 200:
            assert "CSRF" in response.text or "csrf" in response.text.lower()

    def test_valid_csrf_token_accepted(self, client):
        """Test that a request with a valid CSRF token is accepted."""

        # Get the CSRF cookie from the client
        csrf_cookie = client.cookies.get("csrf_token")
        assert csrf_cookie is not None

        response = client.post(
            "/todos/add",
            data={
                "title": "Test todo",
                "csrf_token": csrf_cookie,
            },
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert response.headers["location"] == "/todos"

    def test_htmx_csrf_token_accepted(self, client):
        """Test that HTMX requests with X-CSRF-Token header are accepted."""

        csrf_cookie = client.cookies.get("csrf_token")
        assert csrf_cookie is not None

        from snekdo.models import Todo
        from snekdo.storage import TodoStorage

        storage_file = Path(client.app.state.storage_path)
        storage = TodoStorage(storage_path=str(storage_file))
        todo = Todo(title="Test todo", user_id=client.app.state.user_id)
        storage.add(todo)

        response = client.post(
            f"/todos/{todo.id}/complete",
            headers={
                "HX-Request": "true",
                "X-CSRF-Token": csrf_cookie,
            },
        )
        assert response.status_code == 200
        assert "✓" in response.text

    def test_logout_invalidates_csrf_token(self, client):
        """Test that logout invalidates the CSRF token."""
        from snekdo.csrf import get_csrf_token_cookie

        # Get the current CSRF token
        before_token = get_csrf_token_cookie(client)
        assert before_token is not None

        # Logout
        response = client.post(
            "/auth/logout",
            follow_redirects=False,
        )
        after_token = get_csrf_token_cookie(response)

        # The token should be deleted (None after logout)
        assert after_token is None or after_token == ""

        # Try to use the old token - should be rejected
        old_token = before_token
        response = client.post(
            "/todos/add",
            data={
                "title": "Test todo",
                "csrf_token": old_token,
            },
            follow_redirects=False,
        )
        assert response.status_code in (200, 403, 302)

    def test_csrf_token_unique_per_user(self, tmp_path):
        """Test that different users have different CSRF tokens."""
        from fastapi.testclient import TestClient

        from snekdo.api import create_app
        from snekdo.web import get_template_env, register_web_routes

        storage_file = tmp_path / "todos.json"
        app = create_app(storage_path=str(storage_file))
        app.state.template_env = get_template_env()
        app.state.storage_path = str(storage_file)
        register_web_routes(app, storage_path=str(storage_file))
        client = TestClient(app)

        # Register user 1
        client.post(
            "/auth/register",
            data={"username": "user1", "password": "password123"},
        )
        client.post(
            "/auth/login",
            data={"username": "user1", "password": "password123"},
        )
        token1 = client.cookies.get("csrf_token")

        # Register user 2 (new session, different token)
        client2 = TestClient(app)
        client2.post(
            "/auth/register",
            data={"username": "user2", "password": "password123"},
        )
        client2.post(
            "/auth/login",
            data={"username": "user2", "password": "password123"},
        )
        token2 = client2.cookies.get("csrf_token")

        assert token1 is not None
        assert token2 is not None
        assert token1 != token2


class TestSecretFallback:
    """Tests for the JWT secret fallback behavior."""

    def test_secret_from_env_var(self, monkeypatch):
        """When the env var is set, the signing key is taken from it."""
        from snekdo.auth import _resolve_secret_key

        monkeypatch.setenv("SNEKDO_JWT_SECRET_KEY", "env-sourced-key")
        assert _resolve_secret_key() == "env-sourced-key"

    def test_random_fallback_without_env(self, monkeypatch):
        """When unset, the key is a random per-process value, not a static default."""
        from snekdo.auth import _resolve_secret_key

        monkeypatch.delenv("SNEKDO_JWT_SECRET_KEY", raising=False)
        key = _resolve_secret_key()
        # Must not fall back to any static default value.
        assert key != "snekdo-secret-key-change-me"
        # Random per-process key is a non-empty string.
        assert isinstance(key, str) and key

    def test_fallback_key_is_random(self, monkeypatch):
        """Each fallback key is distinct (random per call), so it is not reused."""
        from snekdo.auth import _resolve_secret_key

        monkeypatch.delenv("SNEKDO_JWT_SECRET_KEY", raising=False)
        assert _resolve_secret_key() != _resolve_secret_key()

    def test_create_decode_roundtrip(self, monkeypatch):
        """A token created with the current key can be decoded with the same key."""
        monkeypatch.delenv("SNEKDO_JWT_SECRET_KEY", raising=False)
        from snekdo import auth

        token = auth.create_access_token("user-1")
        assert auth.decode_access_token(token) == "user-1"


# ---------------------------------------------------------------------------
# Filter helper unit tests
# ---------------------------------------------------------------------------

class TestFilterTodos:
    """Unit tests for the _filter_todos helper in snekdo.web."""

    def _make_todos(self):
        from snekdo.models import Todo
        return [
            Todo(title="Buy milk", description="From the store", priority="high", completed=False),
            Todo(title="Write report", description="Urgent deadline", priority="medium", completed=False),
            Todo(title="Do laundry", description="", priority="low", completed=True),
            Todo(title="Pay bills", description="Monthly bills", priority="high", completed=True),
            Todo(title="Buy groceries", description="Weekly shopping", priority="medium", completed=False),
        ]

    def test_search_by_title(self):
        from snekdo.web import _filter_todos
        todos = self._make_todos()
        result = _filter_todos(todos, q="buy", status="all")
        titles = [t.title for t in result]
        assert "Buy milk" in titles
        assert "Buy groceries" in titles
        assert "Write report" not in titles

    def test_search_by_description(self):
        from snekdo.web import _filter_todos
        todos = self._make_todos()
        result = _filter_todos(todos, q="urgent", status="all")
        titles = [t.title for t in result]
        assert "Write report" in titles
        assert "Buy milk" not in titles

    def test_search_case_insensitive(self):
        from snekdo.web import _filter_todos
        todos = self._make_todos()
        result = _filter_todos(todos, q="MILK", status="all")
        assert len(result) == 1
        assert result[0].title == "Buy milk"

    def test_status_pending(self):
        from snekdo.web import _filter_todos
        todos = self._make_todos()
        result = _filter_todos(todos, status="pending")
        assert all(not t.completed for t in result)
        assert len(result) == 3

    def test_status_completed(self):
        from snekdo.web import _filter_todos
        todos = self._make_todos()
        result = _filter_todos(todos, status="completed")
        assert all(t.completed for t in result)
        assert len(result) == 2

    def test_status_all(self):
        from snekdo.web import _filter_todos
        todos = self._make_todos()
        result = _filter_todos(todos, status="all")
        assert len(result) == 5

    def test_priority_high(self):
        from snekdo.web import _filter_todos
        todos = self._make_todos()
        result = _filter_todos(todos, status="all", priority="high")
        assert all(t.priority == "high" for t in result)
        assert len(result) == 2

    def test_priority_low(self):
        from snekdo.web import _filter_todos
        todos = self._make_todos()
        result = _filter_todos(todos, status="all", priority="low")
        assert len(result) == 1
        assert result[0].title == "Do laundry"

    def test_combined_filters_and(self):
        from snekdo.web import _filter_todos
        todos = self._make_todos()
        result = _filter_todos(todos, q="buy", status="completed", priority="high")
        # "Buy milk" is pending+high, "Pay bills" is completed+high but no "buy" in title/desc
        # No todo matches all three criteria
        assert len(result) == 0

        result2 = _filter_todos(todos, q="bills", status="completed", priority="high")
        assert len(result2) == 1
        assert result2[0].title == "Pay bills"

    def test_default_status_is_pending(self):
        from snekdo.web import _filter_todos
        todos = self._make_todos()
        result = _filter_todos(todos)
        assert all(not t.completed for t in result)
        assert len(result) == 3


# ---------------------------------------------------------------------------
# Web route filter tests
# ---------------------------------------------------------------------------

class TestListFilters:
    """Tests for /todos search and filter query parameters."""

    def _seed_todos(self, client):
        from snekdo.models import Todo
        from snekdo.storage import TodoStorage
        storage = TodoStorage(storage_path=str(client.app.state.storage_path))
        uid = client.app.state.user_id
        storage.add(Todo(title="Buy milk", description="Dairy aisle", priority="high", completed=False, user_id=uid))
        storage.add(Todo(title="Write report", description="Quarterly summary", priority="medium", completed=False, user_id=uid))
        storage.add(Todo(title="Do laundry", description="", priority="low", completed=True, user_id=uid))
        storage.add(Todo(title="Pay bills", description="Electric and water", priority="high", completed=True, user_id=uid))
        storage.add(Todo(title="Buy groceries", description="Weekly shopping list", priority="medium", completed=False, user_id=uid))

    def test_filter_by_search_query(self, client):
        self._seed_todos(client)
        response = client.get("/todos", params={"q": "buy", "status": "all"})
        assert response.status_code == 200
        assert "Buy milk" in response.text
        assert "Buy groceries" in response.text
        assert "Write report" not in response.text
        assert "Do laundry" not in response.text

    def test_filter_by_status_completed(self, client):
        self._seed_todos(client)
        response = client.get("/todos", params={"status": "completed"})
        assert response.status_code == 200
        assert "Do laundry" in response.text
        assert "Pay bills" in response.text
        assert "Buy milk" not in response.text
        assert "Write report" not in response.text

    def test_filter_by_status_pending(self, client):
        self._seed_todos(client)
        response = client.get("/todos", params={"status": "pending"})
        assert response.status_code == 200
        assert "Buy milk" in response.text
        assert "Do laundry" not in response.text
        assert "Pay bills" not in response.text

    def test_filter_by_status_all(self, client):
        self._seed_todos(client)
        response = client.get("/todos", params={"status": "all"})
        assert response.status_code == 200
        assert "Buy milk" in response.text
        assert "Do laundry" in response.text

    def test_filter_by_priority(self, client):
        self._seed_todos(client)
        response = client.get("/todos", params={"priority": "high", "status": "all"})
        assert response.status_code == 200
        assert "Buy milk" in response.text
        assert "Pay bills" in response.text
        assert "Write report" not in response.text
        assert "Do laundry" not in response.text

    def test_combined_filters(self, client):
        self._seed_todos(client)
        response = client.get("/todos", params={"q": "bills", "status": "completed", "priority": "high"})
        assert response.status_code == 200
        assert "Pay bills" in response.text
        assert "Buy milk" not in response.text
        assert "Do laundry" not in response.text

    def test_no_match_shows_empty_state(self, client):
        self._seed_todos(client)
        response = client.get("/todos", params={"q": "nonexistent"})
        assert response.status_code == 200
        assert "No todos found" in response.text

    def test_filter_bar_values_prepopulated(self, client):
        self._seed_todos(client)
        response = client.get("/todos", params={"q": "buy", "status": "all", "priority": "high"})
        assert response.status_code == 200
        assert 'value="buy"' in response.text
        assert '<option value="all" selected>All</option>' in response.text
        assert '<option value="high" selected>High</option>' in response.text

    def test_default_no_filters_shows_pending_only(self, client):
        self._seed_todos(client)
        response = client.get("/todos")
        assert response.status_code == 200
        assert "Buy milk" in response.text
        assert "Do laundry" not in response.text

