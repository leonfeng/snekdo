"""Tests for the FastAPI REST API."""

import json
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from snekdo.api import create_app
from snekdo.storage import TodoStorage


def _make_todo(title: str = "Test todo", description: str = "A test todo", due: str = "2025-12-31", priority: str = "medium"):
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


def test_health_check(tmp_path: Path):
    """Test the health check endpoint returns 200 with status ok."""
    storage = TodoStorage(storage_path=str(tmp_path / "todos.json"))
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

    response = client.get("/api/v1/todos")

    assert response.status_code == 200
    assert response.json() == []


def test_list_todos_with_data(tmp_path: Path):
    """Test listing todos returns the stored todos."""
    from snekdo.models import Todo
    storage = TodoStorage(storage_path=str(tmp_path / "todos.json"))
    todo = _make_todo()
    storage.add(todo)

    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    response = client.get("/api/v1/todos")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == todo.id
    assert data[0]["title"] == todo.title


def test_show_todo(tmp_path: Path):
    """Test showing a single todo by ID."""
    from snekdo.models import Todo
    storage = TodoStorage(storage_path=str(tmp_path / "todos.json"))
    todo = _make_todo()
    storage.add(todo)

    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    response = client.get(f"/api/v1/todos/{todo.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo.id
    assert data["title"] == todo.title


def test_show_todo_not_found(tmp_path: Path):
    """Test showing a non-existent todo returns 404."""
    app = create_app()
    client = TestClient(app)

    response = client.get("/api/v1/todos/non-existent-id")

    assert response.status_code == 404


def test_add_todo(tmp_path: Path):
    """Test adding a new todo via the API."""
    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    response = client.post(
        "/api/v1/todos",
        json={"title": "New todo", "description": "A new todo item", "due": "2027-12-31", "priority": "high"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New todo"
    assert data["description"] == "A new todo item"
    assert data["priority"] == "high"
    assert data["completed"] is False


def test_add_todo_missing_title(tmp_path: Path):
    """Test adding a todo without a title returns 422."""
    app = create_app()
    client = TestClient(app)

    response = client.post("/api/v1/todos", json={"description": "No title"})

    assert response.status_code == 422


def test_add_todo_invalid_due_date(tmp_path: Path):
    """Test adding a todo with an invalid due date returns 422."""
    app = create_app()
    client = TestClient(app)

    response = client.post(
        "/api/v1/todos",
        json={"title": "Bad date", "due": "not-a-date"},
    )

    assert response.status_code == 422


def test_complete_todo(tmp_path: Path):
    """Test marking a todo as complete."""
    from snekdo.models import Todo
    storage = TodoStorage(storage_path=str(tmp_path / "todos.json"))
    todo = _make_todo()
    storage.add(todo)

    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    response = client.post(f"/api/v1/todos/{todo.id}/complete")

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True


def test_complete_todo_not_found(tmp_path: Path):
    """Test completing a non-existent todo returns 404."""
    app = create_app()
    client = TestClient(app)

    response = client.post("/api/v1/todos/non-existent-id/complete")

    assert response.status_code == 404


def test_modify_todo(tmp_path: Path):
    """Test modifying an existing todo."""
    from snekdo.models import Todo
    storage = TodoStorage(storage_path=str(tmp_path / "todos.json"))
    todo = _make_todo()
    storage.add(todo)

    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    response = client.put(
        f"/api/v1/todos/{todo.id}",
        json={"title": "Updated title", "description": "Updated description"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["description"] == "Updated description"


def test_modify_todo_not_found(tmp_path: Path):
    """Test modifying a non-existent todo returns 404."""
    app = create_app()
    client = TestClient(app)

    response = client.put("/api/v1/todos/non-existent-id", json={"title": "Updated"})

    assert response.status_code == 404


def test_delete_todo(tmp_path: Path):
    """Test deleting a todo."""
    from snekdo.models import Todo
    storage = TodoStorage(storage_path=str(tmp_path / "todos.json"))
    todo = _make_todo()
    storage.add(todo)

    app = create_app(storage_path=str(tmp_path / "todos.json"))
    client = TestClient(app)

    response = client.delete(f"/api/v1/todos/{todo.id}")

    assert response.status_code == 200
    data = response.json()
    assert "Deleted" in data["message"]


def test_delete_todo_not_found(tmp_path: Path):
    """Test deleting a non-existent todo returns 404."""
    app = create_app()
    client = TestClient(app)

    response = client.delete("/api/v1/todos/non-existent-id")

    assert response.status_code == 404


def test_custom_storage_path(tmp_path: Path):
    """Test that the API uses the custom storage path."""
    from snekdo.models import Todo
    storage = TodoStorage(storage_path=str(tmp_path / "custom_todos.json"))
    todo = _make_todo()
    storage.add(todo)

    app = create_app(storage_path=str(tmp_path / "custom_todos.json"))
    client = TestClient(app)

    response = client.get("/api/v1/todos")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == todo.title


def test_openapi_schema(tmp_path: Path):
    """Test the OpenAPI schema endpoint."""
    app = create_app()
    client = TestClient(app)

    response = client.get("/openapi.json")

    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert data["openapi"].startswith("3.")
