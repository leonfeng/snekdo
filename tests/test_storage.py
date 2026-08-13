"""Tests for the TodoStorage class."""

import json
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
