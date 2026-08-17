"""Tests for the Todo and User models."""

from snekdo.models import Todo, User


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


# ---------------------------------------------------------------------------
# User model
# ---------------------------------------------------------------------------

def test_user_to_dict():
    """Test that User.to_dict includes display_name and email."""
    user = User(
        id="1",
        username="testuser",
        display_name="Test User",
        email="test@example.com",
        password_hash="$2b$12$...",
        created_at="2024-01-01T00:00:00",
    )
    data = user.to_dict()
    assert data["id"] == "1"
    assert data["username"] == "testuser"
    assert data["display_name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert data["created_at"] == "2024-01-01T00:00:00"


def test_user_from_dict():
    """Test that User.from_dict deserializes display_name and email."""
    data = {
        "id": "1",
        "username": "testuser",
        "display_name": "Test User",
        "email": "test@example.com",
        "password_hash": "$2b$12$...",
        "created_at": "2024-01-01T00:00:00",
    }
    user = User.from_dict(data)
    assert user.id == "1"
    assert user.username == "testuser"
    assert user.display_name == "Test User"
    assert user.email == "test@example.com"
    assert user.created_at == "2024-01-01T00:00:00"


def test_user_from_dict_defaults():
    """Test that User.from_dict uses defaults for display_name and email."""
    data = {
        "id": "1",
        "username": "testuser",
        "password_hash": "$2b$12$...",
        "created_at": "2024-01-01T00:00:00",
    }
    user = User.from_dict(data)
    assert user.display_name == ""
    assert user.email == ""


def test_user_from_dict_backward_compatible():
    """Test that from_dict works with old format (no display_name/email fields)."""
    data = {
        "id": "1",
        "username": "testuser",
        "password_hash": "$2b$12$...",
        "created_at": "2024-01-01T00:00:00",
    }
    user = User.from_dict(data)
    assert user.display_name == ""
    assert user.email == ""


def test_user_default_id_generation():
    """Test that a User gets a default ID if none is provided."""
    user = User(username="testuser")
    assert user.id != ""


# ---------------------------------------------------------------------------
# Todo user_id serialization
# ---------------------------------------------------------------------------

def test_todo_to_dict_includes_user_id():
    """Test that to_dict always includes the user_id key (even when None)."""
    todo = Todo(
        id="1",
        title="Test",
        description="",
        due=None,
        completed=False,
        created_at="2024-01-01T00:00:00",
        user_id="user123",
    )
    data = todo.to_dict()
    assert "user_id" in data
    assert data["user_id"] == "user123"


def test_todo_to_dict_includes_none_user_id():
    """Test that to_dict includes user_id key even when it is None."""
    todo = Todo(
        id="2",
        title="Test",
        description="",
        due=None,
        completed=False,
        created_at="2024-01-01T00:00:00",
    )
    data = todo.to_dict()
    assert "user_id" in data
    assert data["user_id"] is None


def test_todo_from_dict_with_user_id():
    """Test that from_dict handles user_id when present."""
    data = {
        "id": "1",
        "title": "Test",
        "description": "",
        "due": None,
        "completed": False,
        "created_at": "2024-01-01T00:00:00",
        "user_id": "user123",
    }
    todo = Todo.from_dict(data)
    assert todo.user_id == "user123"


def test_todo_from_dict_without_user_id():
    """Test that from_dict handles missing user_id (backward compatibility)."""
    data = {
        "id": "1",
        "title": "Test",
        "description": "",
        "due": None,
        "completed": False,
        "created_at": "2024-01-01T00:00:00",
    }
    todo = Todo.from_dict(data)
    assert todo.user_id is None


def test_todo_roundtrip_with_user_id():
    """Test that a todo with user_id roundtrips through to_dict/from_dict."""
    todo = Todo(
        id="1",
        title="Test",
        description="",
        due=None,
        completed=False,
        created_at="2024-01-01T00:00:00",
        user_id="user123",
    )
    data = todo.to_dict()
    restored = Todo.from_dict(data)
    assert restored.id == todo.id
    assert restored.title == todo.title
    assert restored.user_id == todo.user_id
