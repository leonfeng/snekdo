"""Fix storage.py - proper context manager implementation."""

from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, List, Optional

from snekdo.models import Todo

try:
    import fcntl
except ImportError:
    import fake_fcntl as fcntl  # type: ignore[import-not-found]


class StorageError(Exception):
    """Raised when a storage operation fails."""


class TodoStorage:
    """Manages reading and writing todos to a JSON file."""

    def __init__(self, storage_path: Optional[str] = None) -> None:
        if storage_path is not None:
            self.storage_path = Path(storage_path)
        else:
            self.storage_path = Path.home() / ".snekdo" / "todos.json"

    def _ensure_dir(self) -> None:
        """Create the storage directory if it does not exist."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def _open_file(self, path: Path, mode: str) -> Iterator:
        """Open a file with file locking for write operations."""
        f = open(path, mode)
        if "w" in mode:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                yield f
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
        else:
            fcntl.flock(f, fcntl.LOCK_SH)
            try:
                yield f
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
        f.close()

    def load(self) -> List[Todo]:
        """Load all todos from the JSON file.

        Returns an empty list if the file does not exist.
        """
        if not self.storage_path.exists():
            return []
        with self._open_file(self.storage_path, "r") as f:
            data = json.load(f)
        return [Todo.from_dict(todo) for todo in data]

    def save(self, todos: List[Todo]) -> None:
        """Save all todos to the JSON file."""
        self._ensure_dir()
        with self._open_file(self.storage_path, "w") as f:
            json.dump([todo.to_dict() for todo in todos], f, indent=2)

    def add(self, todo: Todo) -> None:
        """Append a todo and persist."""
        todos = self.load()
        todos.append(todo)
        self.save(todos)

    def get(self, todo_id: str) -> Optional[Todo]:
        """Find a todo by ID.

        Returns None if not found.
        """
        return self.get_all().get(todo_id)

    def delete(self, todo_id: str) -> bool:
        """Remove a todo by ID.

        Returns True if the todo was found and deleted.
        """
        todos = self.load()
        before = len(todos)
        todos = [t for t in todos if t.id != todo_id]
        if len(todos) == before:
            return False
        self.save(todos)
        return True

    def complete(self, todo_id: str) -> bool:
        """Mark a todo as complete by ID.

        Returns True if the todo was found and updated.
        """
        todos = self.load()
        for todo in todos:
            if todo.id == todo_id:
                todo.completed = True
                self.save(todos)
                return True
        return False

    def get_all(self) -> dict:
        """Return all todos as a dict keyed by ID."""
        return {todo.id: todo for todo in self.load()}
