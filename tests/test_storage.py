"""Tests for the TodoStorage class."""

import tempfile
from pathlib import Path

import pytest

from snekdo.models import Todo, User
from snekdo.storage import StorageError, TodoStorage, UserStorage


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


def test_complete_non_recurring_does_not_duplicate():
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todo = Todo(
            id="1",
            title="One-off",
            description="",
            due="2024-12-31",
            completed=False,
            created_at="2024-01-01T00:00:00",
        )
        storage.add(todo)
        storage.complete("1")
        todos = storage.load()
        assert len(todos) == 1
        assert todos[0].completed is True


def test_complete_daily_recurring_creates_next_occurrence():
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todo = Todo(
            id="1",
            title="Daily task",
            description="",
            due="2024-06-01",
            completed=False,
            created_at="2024-01-01T00:00:00",
            repeat="daily",
        )
        storage.add(todo)
        result = storage.complete("1")
        assert result is True
        todos = storage.load()
        assert len(todos) == 2
        completed = [t for t in todos if t.completed]
        pending = [t for t in todos if not t.completed]
        assert len(completed) == 1
        assert completed[0].id == "1"
        assert completed[0].last_completed_at is not None
        assert len(pending) == 1
        assert pending[0].id != "1"
        assert pending[0].title == "Daily task"
        assert pending[0].repeat == "daily"
        assert pending[0].due is not None
        assert pending[0].due > "2024-06-01"


def test_complete_weekly_recurring_preserves_other_fields():
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todo = Todo(
            id="1",
            title="Weekly task",
            description="desc",
            due="2024-06-05",
            completed=False,
            created_at="2024-01-01T00:00:00",
            priority="high",
            repeat="weekly",
        )
        storage.add(todo)
        storage.complete("1")
        todos = storage.load()
        pending = [t for t in todos if not t.completed]
        assert len(pending) == 1
        assert pending[0].description == "desc"
        assert pending[0].priority == "high"
        assert pending[0].repeat == "weekly"
        assert pending[0].last_completed_at is None


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
        result = storage.modify("1", title="New Title", description="New Desc", due="2025-01-01")  # noqa: E501
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
        assert updated.due is None


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


def test_modify_tags():
    """Test modifying a todo's tags (replaces the full list)."""
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
            tags=["old"],
        )
        storage.add(todo)
        result = storage.modify("1", tags=["x", "y"])
        assert result is True
        updated = storage.get("1")
        assert updated.tags == ["x", "y"]


def test_modify_category():
    """Test modifying a todo's category."""
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
        )
        storage.add(todo)
        result = storage.modify("1", category="home")
        assert result is True
        updated = storage.get("1")
        assert updated.category == "home"


def test_modify_clear_category():
    """Test clearing a todo's category by setting it to None."""
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
            category="home",
        )
        storage.add(todo)
        result = storage.modify("1", category=None)
        assert result is True
        updated = storage.get("1")
        assert updated.category is None


def test_save_load_tags_category_roundtrip_json():
    """Test tags and category survive a JSON save/load round-trip."""
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
            tags=["a", "b"],
            category="home",
        )
        storage.save([todo])
        todos = storage.load()
        assert len(todos) == 1
        assert todos[0].tags == ["a", "b"]
        assert todos[0].category == "home"


def test_load_old_json_without_tags_category():
    """Test that old-format JSON (no tags/category keys) loads with defaults."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage_path.write_text(
            '[{"id": "1", "title": "Old", "description": "", "due": null, '
            '"completed": false, "created_at": "2024-01-01T00:00:00", '
            '"priority": "medium"}]'
        )
        storage = TodoStorage(storage_path=str(storage_path))
        todos = storage.load()
        assert len(todos) == 1
        assert todos[0].tags == []
        assert todos[0].category is None


def test_complete_recurring_copies_tags_category_json():
    """Test that recurring completion copies tags and category to the next occurrence (JSON)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        todo = Todo(
            id="1",
            title="Recurring",
            description="",
            due="2024-06-01",
            completed=False,
            created_at="2024-01-01T00:00:00",
            repeat="daily",
            tags=["work"],
            category="office",
        )
        storage.add(todo)
        storage.complete("1")
        todos = storage.load()
        pending = [t for t in todos if not t.completed]
        assert len(pending) == 1
        assert pending[0].tags == ["work"]
        assert pending[0].category == "office"


# ---------------------------------------------------------------------------
# SQLite backend
# ---------------------------------------------------------------------------

def _make_sqlite_storage(tmpdir: str) -> tuple[TodoStorage, Path]:
    db_path = Path(tmpdir) / "todos.db"
    return TodoStorage(storage_path=str(db_path), storage_type="sqlite"), db_path


def test_sqlite_save_load_tags_category_roundtrip():
    """Test tags and category survive a SQLite save/load round-trip."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage, _ = _make_sqlite_storage(tmpdir)
        todo = Todo(
            id="1",
            title="Test",
            description="",
            due=None,
            completed=False,
            created_at="2024-01-01T00:00:00",
            tags=["a", "b"],
            category="home",
        )
        storage.save([todo])
        todos = storage.load()
        assert len(todos) == 1
        assert todos[0].tags == ["a", "b"]
        assert todos[0].category == "home"


def test_sqlite_get_tags_category():
    """Test that get() returns tags and category from SQLite."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage, _ = _make_sqlite_storage(tmpdir)
        todo = Todo(
            id="1",
            title="Test",
            description="",
            due=None,
            completed=False,
            created_at="2024-01-01T00:00:00",
            tags=["x"],
            category="work",
        )
        storage.add(todo)
        result = storage.get("1")
        assert result is not None
        assert result.tags == ["x"]
        assert result.category == "work"


def test_sqlite_modify_tags():
    """Test modifying tags via the SQLite backend."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage, _ = _make_sqlite_storage(tmpdir)
        todo = Todo(
            id="1",
            title="Test",
            description="",
            due=None,
            completed=False,
            created_at="2024-01-01T00:00:00",
            tags=["old"],
        )
        storage.add(todo)
        result = storage.modify("1", tags=["x", "y"])
        assert result is True
        updated = storage.get("1")
        assert updated.tags == ["x", "y"]


def test_sqlite_modify_category():
    """Test modifying category via the SQLite backend."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage, _ = _make_sqlite_storage(tmpdir)
        todo = Todo(
            id="1",
            title="Test",
            description="",
            due=None,
            completed=False,
            created_at="2024-01-01T00:00:00",
        )
        storage.add(todo)
        result = storage.modify("1", category="home")
        assert result is True
        updated = storage.get("1")
        assert updated.category == "home"


def test_sqlite_modify_clear_category():
    """Test clearing category via the SQLite backend."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage, _ = _make_sqlite_storage(tmpdir)
        todo = Todo(
            id="1",
            title="Test",
            description="",
            due=None,
            completed=False,
            created_at="2024-01-01T00:00:00",
            category="home",
        )
        storage.add(todo)
        result = storage.modify("1", category=None)
        assert result is True
        updated = storage.get("1")
        assert updated.category is None


def test_sqlite_migration_existing_db():
    """Test that a pre-existing DB without tags/category columns migrates in place."""
    import sqlite3

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "todos.db"
        # Create an old-schema DB with a row
        conn = sqlite3.connect(str(db_path))
        conn.execute(
            """CREATE TABLE todos (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                due TEXT,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                priority TEXT NOT NULL DEFAULT 'medium',
                user_id TEXT,
                repeat TEXT NOT NULL DEFAULT 'none',
                last_completed_at TEXT
            )"""
        )
        conn.execute(
            "INSERT INTO todos (id, title, description, due, completed, created_at, priority, user_id, repeat, last_completed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("1", "Old Todo", "", None, 0, "2024-01-01T00:00:00", "medium", None, "none", None),
        )
        conn.commit()
        conn.close()

        # Initialize the storage against the old DB — migration should add columns
        storage = TodoStorage(storage_path=str(db_path), storage_type="sqlite")
        todos = storage.load()
        assert len(todos) == 1
        assert todos[0].id == "1"
        assert todos[0].title == "Old Todo"
        assert todos[0].tags == []
        assert todos[0].category is None

        # Verify the columns exist in the schema
        conn = sqlite3.connect(str(db_path))
        cols = [row[1] for row in conn.execute("PRAGMA table_info(todos)").fetchall()]
        conn.close()
        assert "tags" in cols
        assert "category" in cols


def test_sqlite_complete_recurring_copies_tags_category():
    """Test that recurring completion copies tags and category in SQLite."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage, _ = _make_sqlite_storage(tmpdir)
        todo = Todo(
            id="1",
            title="Recurring",
            description="",
            due="2024-06-01",
            completed=False,
            created_at="2024-01-01T00:00:00",
            repeat="daily",
            tags=["work"],
            category="office",
        )
        storage.add(todo)
        storage.complete("1")
        todos = storage.load()
        pending = [t for t in todos if not t.completed]
        assert len(pending) == 1
        assert pending[0].tags == ["work"]
        assert pending[0].category == "office"


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


def test_load_corrupted_json():
    """Test that loading a corrupted JSON file returns an empty list."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        storage = TodoStorage(storage_path=str(storage_path))
        # Write corrupted JSON (truncated last entry with extra field)
        storage_path.write_text(
            '[{"id": "1", "title": "Test", "description": "", "due": "2024-12-31", "completed": false, "created_at": "2024-01-01T00:00:00", "priority": "medium"},\n  {"id": "2", "title": "Bad", "due": "2024-12-31", "completed": false, "created_at": "2024-01-01T00:00:00", "priority": "medium", "user_id": '  # noqa: E501
        )
        todos = storage.load()
        assert todos == []


# ---------------------------------------------------------------------------
# UserStorage
# ---------------------------------------------------------------------------

def test_user_storage_add_and_get():
    """Test adding and getting a user."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "users.json"
        storage = UserStorage(storage_path=str(storage_path))
        user = User(
            id="1",
            username="testuser",
            display_name="Test User",
            email="test@example.com",
            password_hash="$2b$12$...",
            created_at="2024-01-01T00:00:00",
        )
        storage.add(user)
        result = storage.get("testuser")
        assert result is not None
        assert result.username == "testuser"
        assert result.display_name == "Test User"
        assert result.email == "test@example.com"


def test_user_storage_get_by_id():
    """Test getting a user by ID."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "users.json"
        storage = UserStorage(storage_path=str(storage_path))
        user = User(
            id="1",
            username="testuser",
            display_name="Test User",
            email="test@example.com",
            password_hash="$2b$12$...",
            created_at="2024-01-01T00:00:00",
        )
        storage.add(user)
        result = storage.get_by_id("1")
        assert result is not None
        assert result.id == "1"


def test_user_storage_update_profile():
    """Test updating a user's profile."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "users.json"
        storage = UserStorage(storage_path=str(storage_path))
        user = User(
            id="1",
            username="testuser",
            display_name="Original",
            email="original@example.com",
            password_hash="$2b$12$...",
            created_at="2024-01-01T00:00:00",
        )
        storage.add(user)
        result = storage.update_profile("1", display_name="New Name", email="new@example.com")  # noqa: E501
        assert result is True
        updated = storage.get_by_id("1")
        assert updated.display_name == "New Name"
        assert updated.email == "new@example.com"


def test_user_storage_update_profile_partial():
    """Test updating only the display name."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "users.json"
        storage = UserStorage(storage_path=str(storage_path))
        user = User(
            id="1",
            username="testuser",
            display_name="Original",
            email="original@example.com",
            password_hash="$2b$12$...",
            created_at="2024-01-01T00:00:00",
        )
        storage.add(user)
        result = storage.update_profile("1", display_name="New Name")
        assert result is True
        updated = storage.get_by_id("1")
        assert updated.display_name == "New Name"
        assert updated.email == "original@example.com"


def test_user_storage_update_profile_not_found():
    """Test updating a non-existent user returns False."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "users.json"
        storage = UserStorage(storage_path=str(storage_path))
        result = storage.update_profile("nonexistent", display_name="New Name")
        assert result is False


def test_user_storage_update_password():
    """Test updating a user's password."""
    from snekdo.auth import hash_password, verify_password

    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "users.json"
        storage = UserStorage(storage_path=str(storage_path))
        original_password = "old_password"
        user = User(
            id="1",
            username="testuser",
            display_name="Test User",
            email="test@example.com",
            password_hash=hash_password(original_password),
            created_at="2024-01-01T00:00:00",
        )
        storage.add(user)
        result = storage.update_password("1", current_password=original_password, new_password="new_password")  # noqa: E501
        assert result is True
        updated = storage.get_by_id("1")
        assert verify_password("new_password", updated.password_hash)
        assert not verify_password(original_password, updated.password_hash)


def test_user_storage_update_password_wrong_current():
    """Test updating password with wrong current password raises StorageError."""
    from snekdo.auth import hash_password

    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "users.json"
        storage = UserStorage(storage_path=str(storage_path))
        user = User(
            id="1",
            username="testuser",
            display_name="Test User",
            email="test@example.com",
            password_hash=hash_password("correct_password"),
            created_at="2024-01-01T00:00:00",
        )
        storage.add(user)
        with pytest.raises(StorageError):
            storage.update_password("1", current_password="wrong_password", new_password="new_password")  # noqa: E501


def test_user_storage_get_profile():
    """Test get_profile returns user without password hash."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "users.json"
        storage = UserStorage(storage_path=str(storage_path))
        user = User(
            id="1",
            username="testuser",
            display_name="Test User",
            email="test@example.com",
            password_hash="$2b$12$...",
            created_at="2024-01-01T00:00:00",
        )
        storage.add(user)
        profile = storage.get_profile("1")
        assert profile is not None
        assert profile.id == "1"
        assert profile.username == "testuser"
        assert profile.display_name == "Test User"
        assert profile.email == "test@example.com"
        assert profile.password_hash == ""


def test_user_storage_get_profile_not_found():
    """Test get_profile returns None for non-existent user."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "users.json"
        storage = UserStorage(storage_path=str(storage_path))
        result = storage.get_profile("nonexistent")
        assert result is None


def test_user_storage_delete_user_with_todos():
    """Test delete_user_with_todos removes the user and their todos."""
    with tempfile.TemporaryDirectory() as tmpdir:
        todos_path = Path(tmpdir) / "todos.json"
        users_path = Path(tmpdir) / "users.json"
        todo_storage = TodoStorage(storage_path=str(todos_path))
        user_storage = UserStorage(storage_path=str(users_path))

        # Create a user
        user = User(
            id="1",
            username="testuser",
            display_name="Test User",
            email="test@example.com",
            password_hash="$2b$12$...",
            created_at="2024-01-01T00:00:00",
        )
        user_storage.add(user)

        # Create todos for the user
        todo1 = Todo(
            id="1",
            title="Todo 1",
            description="",
            due=None,
            completed=False,
            created_at="2024-01-01T00:00:00",
            user_id="1",
        )
        todo2 = Todo(
            id="2",
            title="Todo 2",
            description="",
            due=None,
            completed=False,
            created_at="2024-01-02T00:00:00",
            user_id="1",
        )
        todo_storage.save([todo1, todo2])

        # Delete the user with their todos
        result = user_storage.delete_user_with_todos("1", todo_storage)
        assert result is True

        # Verify the user is gone
        assert user_storage.get_by_id("1") is None
        # Verify the todos are gone
        assert todo_storage.load() == []


def test_user_storage_delete_user_with_todos_preserves_other_users():
    """Test delete_user_with_todos preserves other users' todos."""
    with tempfile.TemporaryDirectory() as tmpdir:
        todos_path = Path(tmpdir) / "todos.json"
        users_path = Path(tmpdir) / "users.json"
        todo_storage = TodoStorage(storage_path=str(todos_path))
        user_storage = UserStorage(storage_path=str(users_path))

        # Create two users
        user1 = User(
            id="1",
            username="user1",
            display_name="User 1",
            email="user1@example.com",
            password_hash="$2b$12$...",
            created_at="2024-01-01T00:00:00",
        )
        user2 = User(
            id="2",
            username="user2",
            display_name="User 2",
            email="user2@example.com",
            password_hash="$2b$12$...",
            created_at="2024-01-01T00:00:00",
        )
        user_storage.add(user1)
        user_storage.add(user2)

        # Create todos for both users
        todo1 = Todo(
            id="1",
            title="User 1 todo",
            description="",
            due=None,
            completed=False,
            created_at="2024-01-01T00:00:00",
            user_id="1",
        )
        todo2 = Todo(
            id="2",
            title="User 2 todo",
            description="",
            due=None,
            completed=False,
            created_at="2024-01-02T00:00:00",
            user_id="2",
        )
        todo_storage.save([todo1, todo2])

        # Delete user 1 and their todos
        result = user_storage.delete_user_with_todos("1", todo_storage)
        assert result is True

        # Verify user 1 is gone but user 2 remains
        assert user_storage.get_by_id("1") is None
        assert user_storage.get_by_id("2") is not None

        # Verify user 1's todos are gone but user 2's remain
        todos = todo_storage.load()
        assert len(todos) == 1
        assert todos[0].id == "2"
        assert todos[0].title == "User 2 todo"


def test_user_storage_delete_user_with_todos_not_found():
    """Test delete_user_with_todos returns False for non-existent user."""
    with tempfile.TemporaryDirectory() as tmpdir:
        todos_path = Path(tmpdir) / "todos.json"
        users_path = Path(tmpdir) / "users.json"
        todo_storage = TodoStorage(storage_path=str(todos_path))
        user_storage = UserStorage(storage_path=str(users_path))

        # Create a user
        user = User(
            id="1",
            username="testuser",
            display_name="Test User",
            email="test@example.com",
            password_hash="$2b$12$...",
            created_at="2024-01-01T00:00:00",
        )
        user_storage.add(user)

        # Try to delete a non-existent user
        result = user_storage.delete_user_with_todos("nonexistent", todo_storage)
        assert result is False

        # Verify the existing user is still there
        assert user_storage.get_by_id("1") is not None
