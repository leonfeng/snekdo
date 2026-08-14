"""Tests for the TodoStorage class."""

import tempfile
from pathlib import Path

from snekdo.models import Todo
from snekdo.storage import TodoStorage


def test_load_empty_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todos = storage.load()
        assert todos == []


def test_load_nonexistent_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todos = storage.load()
        assert todos == []


def test_save_and_load():
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todo = Todo(
            id="1",
            title="Test",
            description="A test todo",
            due="2024-12-31",
            completed=False,
            created_at="2024-01-01T00:00:00",
        )
        storage.save([todo])
        todos = storage.load()
        assert len(todos) == 1
        assert todos[0].title == "Test"


def test_add():
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todo = Todo(
            id="1",
            title="Test",
            description="A test todo",
            due="2024-12-31",
            completed=False,
            created_at="2024-01-01T00:00:00",
        )
        storage.add(todo)
        todos = storage.load()
        assert len(todos) == 1
        assert todos[0].title == "Test"


def test_get():
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todo = Todo(
            id="1",
            title="Test",
            description="A test todo",
            due="2024-12-31",
            completed=False,
            created_at="2024-01-01T00:00:00",
        )
        storage.add(todo)
        result = storage.get("1")
        assert result is not None
        assert result.title == "Test"


def test_get_not_found():
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        result = storage.get("nonexistent")
        assert result is None


def test_delete():
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todo = Todo(
            id="1",
            title="Test",
            description="A test todo",
            due="2024-12-31",
            completed=False,
            created_at="2024-01-01T00:00:00",
        )
        storage.add(todo)
        result = storage.delete("1")
        assert result is True
        assert storage.get("1") is None


def test_delete_not_found():
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        result = storage.delete("nonexistent")
        assert result is False


def test_complete():
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todo = Todo(
            id="1",
            title="Test",
            description="A test todo",
            due="2024-12-31",
            completed=False,
            created_at="2024-01-01T00:00:00",
        )
        storage.add(todo)
        result = storage.complete("1")
        assert result is True
        updated = storage.get("1")
        assert updated.completed is True


def test_complete_not_found():
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        result = storage.complete("nonexistent")
        assert result is False


def test_modify():
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todo = Todo(
            id="1",
            title="Test",
            description="A test todo",
            due="2024-12-31",
            completed=False,
            created_at="2024-01-01T00:00:00",
        )
        storage.add(todo)
        result = storage.modify("1", title="Updated Title")
        assert result is True
        updated = storage.get("1")
        assert updated.title == "Updated Title"


def test_modify_not_found():
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        result = storage.modify("nonexistent", title="Updated Title")
        assert result is False


def test_modify_multiple_fields():
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todo = Todo(
            id="1",
            title="Test",
            description="A test todo",
            due="2024-12-31",
            completed=False,
            created_at="2024-01-01T00:00:00",
        )
        storage.add(todo)
        result = storage.modify("1", title="New Title", description="New Desc", due="2025-01-01")
        assert result is True
        updated = storage.get("1")
        assert updated.title == "New Title"
        assert updated.description == "New Desc"
        assert updated.due == "2025-01-01"


def test_modify_empty_string_title():
    """Test modifying with an empty string title."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todo = Todo(
            id="1",
            title="Test",
            description="A test todo",
            due="2024-12-31",
            completed=False,
            created_at="2024-01-01T00:00:00",
        )
        storage.add(todo)
        result = storage.modify("1", title="")
        assert result is True
        updated = storage.get("1")
        assert updated.title == ""


def test_modify_clear_description():
    """Test clearing the description by setting it to empty string."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todo = Todo(
            id="1",
            title="Test",
            description="A test todo",
            due="2024-12-31",
            completed=False,
            created_at="2024-01-01T00:00:00",
        )
        storage.add(todo)
        result = storage.modify("1", description="")
        assert result is True
        updated = storage.get("1")
        assert updated.description == ""


def test_modify_clear_due():
    """Test clearing the due date by setting it to empty string."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todo = Todo(
            id="1",
            title="Test",
            description="A test todo",
            due="2024-12-31",
            completed=False,
            created_at="2024-01-01T00:00:00",
        )
        storage.add(todo)
        result = storage.modify("1", due="")
        assert result is True
        updated = storage.get("1")
        assert updated.due == ""


def test_modify_partial_update():
    """Test that modifying one field doesn't affect others."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todo = Todo(
            id="1",
            title="Test",
            description="A test todo",
            due="2024-12-31",
            completed=False,
            created_at="2024-01-01T00:00:00",
        )
        storage.add(todo)
        result = storage.modify("1", title="Updated Title")
        assert result is True
        updated = storage.get("1")
        assert updated.title == "Updated Title"
        assert updated.description == "A test todo"
        assert updated.due == "2024-12-31"


def test_modify_priority():
    """Test modifying a todo's priority."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todo = Todo(
            id="1",
            title="Test",
            description="A test todo",
            due="2024-12-31",
            completed=False,
            created_at="2024-01-01T00:00:00",
            priority="low",
        )
        storage.add(todo)
        result = storage.modify("1", priority="high")
        assert result is True
        updated = storage.get("1")
        assert updated.priority == "high"


def test_filter_by_priority():
    """Test filtering todos by priority."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todo1 = Todo(
            id="1",
            title="High Priority",
            description="",
            due=None,
            completed=False,
            created_at="2024-01-01T00:00:00",
            priority="high",
        )
        todo2 = Todo(
            id="2",
            title="Low Priority",
            description="",
            due=None,
            completed=False,
            created_at="2024-01-02T00:00:00",
            priority="low",
        )
        storage.save([todo1, todo2])
        
        high_priority = storage.filter_by_priority("high")
        assert len(high_priority) == 1
        assert high_priority[0].title == "High Priority"
        
        low_priority = storage.filter_by_priority("low")
        assert len(low_priority) == 1
        assert low_priority[0].title == "Low Priority"


def test_filter_by_priority_not_found():
    """Test filtering by priority when no todos match."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todo = Todo(
            id="1",
            title="Test",
            description="",
            due=None,
            completed=False,
            created_at="2024-01-01T00:00:00",
            priority="high",
        )
        storage.add(todo)
        
        result = storage.filter_by_priority("low")
        assert result == []
