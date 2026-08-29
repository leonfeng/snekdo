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

    # Also verify empty string user_id is normalized to None.
    data["user_id"] = ""
    todo = Todo.from_dict(data)
    assert todo.user_id is None


def test_todo_from_dict_empty_string_user_id():
    """Test that from_dict converts empty string user_id to None."""
    data = {
        "id": "1",
        "title": "Test",
        "description": "",
        "due": None,
        "completed": False,
        "created_at": "2024-01-01T00:00:00",
        "user_id": "",
    }
    todo = Todo.from_dict(data)
    assert todo.user_id is None


def test_todo_from_dict_empty_string_due():
    """Test that from_dict converts empty string due to None."""
    data = {
        "id": "1",
        "title": "Test",
        "description": "",
        "due": "",
        "completed": False,
        "created_at": "2024-01-01T00:00:00",
    }
    todo = Todo.from_dict(data)
    assert todo.due is None


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


def test_next_due_date_daily():
    from datetime import datetime
    from snekdo.models import next_due_date

    # due is in the future relative to now
    assert next_due_date("2024-06-01", "daily", datetime(2024, 6, 1)) == "2024-06-02"
    # due is today -> next is tomorrow
    assert next_due_date("2024-06-01", "daily", datetime(2024, 6, 1)) == "2024-06-02"


def test_next_due_date_daily_past_due_advances_to_today_or_later():
    from datetime import datetime
    from snekdo.models import next_due_date

    # due far in the past: candidate advances day-by-day until >= today
    assert next_due_date("2024-01-01", "daily", datetime(2024, 6, 1)) == "2024-06-01"


def test_next_due_date_daily_no_due_uses_today():
    from datetime import datetime
    from snekdo.models import next_due_date

    assert next_due_date(None, "daily", datetime(2024, 6, 1)) == "2024-06-02"


def test_next_due_date_weekly():
    from datetime import datetime
    from snekdo.models import next_due_date

    assert next_due_date("2024-06-01", "weekly", datetime(2024, 6, 1)) == "2024-06-08"


def test_next_due_date_weekly_past_due():
    from datetime import datetime
    from snekdo.models import next_due_date

    # 2024-05-01 + 7k days; first >= 2024-06-01 is 2024-06-05? 05-01->05-08->...->06-05
    # 05-01, 05-08, 05-15, 05-22, 05-29, 06-05 -> 06-05
    assert next_due_date("2024-05-01", "weekly", datetime(2024, 6, 1)) == "2024-06-05"


def test_next_due_date_monthly():
    from datetime import datetime
    from snekdo.models import next_due_date

    assert next_due_date("2024-06-01", "monthly", datetime(2024, 6, 1)) == "2024-07-01"


def test_next_due_date_monthly_clamps_to_month_end():
    from datetime import datetime
    from snekdo.models import next_due_date

    # Jan 31 -> Feb 28 (2024 is leap year)
    assert next_due_date("2024-01-31", "monthly", datetime(2024, 1, 1)) == "2024-02-29"
    # Jan 31 -> Feb 28 (2023 not leap)
    assert next_due_date("2023-01-31", "monthly", datetime(2023, 1, 1)) == "2023-02-28"


def test_next_due_date_monthly_past_due():
    from datetime import datetime
    from snekdo.models import next_due_date

    # 2024-01-15 monthly, now 2024-06-01: 02-15,03-15,04-15,05-15,06-15
    assert next_due_date("2024-01-15", "monthly", datetime(2024, 6, 1)) == "2024-06-15"


def test_next_due_date_yearly():
    from datetime import datetime
    from snekdo.models import next_due_date

    assert next_due_date("2024-06-01", "yearly", datetime(2024, 6, 1)) == "2025-06-01"


def test_next_due_date_yearly_clamps_feb29():
    from datetime import datetime
    from snekdo.models import next_due_date

    # 2024-02-29 yearly -> 2025-02-28
    assert next_due_date("2024-02-29", "yearly", datetime(2024, 1, 1)) == "2025-02-28"


def test_next_due_date_invalid_repeat_raises():
    import pytest
    from datetime import datetime
    from snekdo.models import next_due_date

    with pytest.raises(ValueError):
        next_due_date("2024-06-01", "none", datetime(2024, 6, 1))
    with pytest.raises(ValueError):
        next_due_date("2024-06-01", "hourly", datetime(2024, 6, 1))
