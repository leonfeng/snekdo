"""Tests for the snekdo web frontend."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from snekdo.api import create_app
from snekdo.web import register_web_routes, get_template_env


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
        todo = Todo(title="Original", description="Old desc", user_id=client.app.state.user_id)
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
