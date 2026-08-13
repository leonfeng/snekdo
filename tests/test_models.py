"""Tests for the Todo model."""

from snekdo.models import Todo


def test_todo_to_dict():
    todo = Todo(
        id="1",
        title="Test",
        description="A test todo",
        due="2024-12-31",
        completed=False,
        created_at="2024-01-01T00:00:00",
    )
    data = todo.to_dict()
    assert data["id"] == "1"
    assert data["title"] == "Test"
    assert data["description"] == "A test todo"
    assert data["due"] == "2024-12-31"
    assert data["completed"] is False
    assert data["created_at"] == "2024-01-01T00:00:00"


def test_todo_from_dict():
    data = {
        "id": "1",
        "title": "Test",
        "description": "A test todo",
        "due": "2024-12-31",
        "completed": False,
        "created_at": "2024-01-01T00:00:00",
    }
    todo = Todo.from_dict(data)
    assert todo.id == "1"
    assert todo.title == "Test"
    assert todo.description == "A test todo"
    assert todo.due == "2024-12-31"
    assert todo.completed is False
    assert todo.created_at == "2024-01-01T00:00:00"


def test_todo_from_dict_defaults():
    data = {
        "id": "1",
        "title": "Test",
        "created_at": "2024-01-01T00:00:00",
    }
    todo = Todo.from_dict(data)
    assert todo.description == ""
    assert todo.due is None
    assert todo.completed is False


def test_todo_default_priority():
    """Test that priority defaults to 'medium'."""
    todo = Todo(
        id="1",
        title="Test",
        description="",
        due=None,
        completed=False,
        created_at="2024-01-01T00:00:00",
    )
    assert todo.priority == "medium"


def test_todo_to_dict_with_priority():
    """Test that to_dict includes priority."""
    todo = Todo(
        id="1",
        title="Test",
        description="",
        due=None,
        completed=False,
        created_at="2024-01-01T00:00:00",
        priority="high",
    )
    data = todo.to_dict()
    assert data["priority"] == "high"


def test_todo_from_dict_with_priority():
    """Test that from_dict handles priority."""
    data = {
        "id": "1",
        "title": "Test",
        "description": "",
        "due": None,
        "completed": False,
        "created_at": "2024-01-01T00:00:00",
        "priority": "high",
    }
    todo = Todo.from_dict(data)
    assert todo.priority == "high"


def test_todo_from_dict_backward_compatible():
    """Test that from_dict works with old format (no priority field)."""
    data = {
        "id": "1",
        "title": "Test",
        "description": "",
        "due": None,
        "completed": False,
        "created_at": "2024-01-01T00:00:00",
    }
    todo = Todo.from_dict(data)
    assert todo.priority == "medium"
