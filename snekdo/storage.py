"""Storage layer for snekdo todos and users."""

from __future__ import annotations

import json
import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, List, Optional

from snekdo.auth import verify_password
from snekdo.models import Todo, User

logger = logging.getLogger(__name__)

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

    def load(self, user_id: Optional[str] = None) -> List[Todo]:
        """Load all todos from the JSON file.

        Returns an empty list if the file does not exist or if the JSON is
        corrupted.  In the latter case a warning is logged so the API keeps
        working even with a bad storage file.

        Args:
            user_id: If provided, filter todos to only those belonging to this user.

        Returns:
            An empty list if the file does not exist.
        """
        if not self.storage_path.exists():
            return []
        try:
            with self._open_file(self.storage_path, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.warning(
                "Storage file %s is corrupted (%s). Returning empty list.",
                self.storage_path,
                e,
            )
            return []
        todos = [Todo.from_dict(todo) for todo in data]
        if user_id is not None:
            todos = [t for t in todos if t.user_id == user_id]
        return todos

    def save(self, todos: List[Todo]) -> None:
        """Save all todos to the JSON file."""
        self._ensure_dir()
        with self._open_file(self.storage_path, "w") as f:
            json.dump([todo.to_dict() for todo in todos], f, indent=2)

    def add(self, todo: Todo) -> None:
        """Append a todo and persist."""
        todos = self.load()
        if todo.user_id is None:
            # Leave user_id as None for backward compatibility with existing todos
            pass
        todos.append(todo)
        self.save(todos)

    def get(self, todo_id: str, user_id: Optional[str] = None) -> Optional[Todo]:
        """Find a todo by ID.

        Args:
            todo_id: The ID of the todo to find.
            user_id: If provided, also filter by user.

        Returns:
            The Todo if found, None otherwise.
        """
        todos = self.load(user_id=user_id)
        for todo in todos:
            if todo.id == todo_id:
                return todo
        return None

    def delete(self, todo_id: str, user_id: Optional[str] = None) -> bool:
        """Remove a todo by ID.

        Args:
            todo_id: The ID of the todo to delete.
            user_id: If provided, also filter by user.

        Returns:
            True if the todo was found and deleted.
        """
        todos = self.load(user_id=user_id)
        before = len(todos)
        todos = [t for t in todos if t.id != todo_id]
        if len(todos) == before:
            return False
        self.save(todos)
        return True

    def complete(self, todo_id: str, user_id: Optional[str] = None) -> bool:
        """Mark a todo as complete by ID.

        Args:
            todo_id: The ID of the todo to complete.
            user_id: If provided, also filter by user.

        Returns:
            True if the todo was found and updated.
        """
        todos = self.load(user_id=user_id)
        for todo in todos:
            if todo.id == todo_id:
                todo.completed = True
                self.save(todos)
                return True
        return False

    def get_all(self, user_id: Optional[str] = None) -> dict:
        """Return all todos as a dict keyed by ID."""
        return {todo.id: todo for todo in self.load(user_id=user_id)}

    def modify(self, todo_id: str, user_id: Optional[str] = None, **kwargs) -> bool:
        """Modify an existing todo by ID.

        Args:
            todo_id: The ID of the todo to modify.
            user_id: If provided, also filter by user.
            **kwargs: Fields to update (title, description, due, priority).

        Returns:
            True if the todo was found and updated, False otherwise.
        """
        todos = self.load(user_id=user_id)
        for todo in todos:
            if todo.id == todo_id:
                # Update only the fields provided
                if "title" in kwargs:
                    todo.title = kwargs["title"]
                if "description" in kwargs:
                    todo.description = kwargs["description"]
                if "due" in kwargs:
                    todo.due = kwargs["due"]
                if "priority" in kwargs:
                    todo.priority = kwargs["priority"]
                self.save(todos)
                return True
        return False

    def filter_by_priority(self, priority: str) -> List[Todo]:
        """Filter todos by priority level.

        Args:
            priority: The priority level to filter by (low, medium, high).

        Returns:
            List of todos matching the given priority.
        """
        todos = self.load()
        return [todo for todo in todos if todo.priority == priority]


class UserStorage:
    """Manages reading and writing users to a JSON file."""

    def __init__(self, storage_path: Optional[str] = None) -> None:
        if storage_path is not None:
            # Derive the users file path from the todos file path.
            # If the path ends with 'todos.json', replace with 'users.json'.
            path = Path(storage_path)
            if path.name == "todos.json":
                self.storage_path = path.with_name("users.json")
            else:
                self.storage_path = path.parent / "users.json"
        else:
            self.storage_path = Path.home() / ".snekdo" / "users.json"

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

    def load(self) -> List[User]:
        """Load all users from the JSON file.

        Returns:
            An empty list if the file does not exist.
        """
        if not self.storage_path.exists():
            return []
        with self._open_file(self.storage_path, "r") as f:
            data = json.load(f)
        return [User.from_dict(user) for user in data]

    def save(self, users: List[User]) -> None:
        """Save all users to the JSON file."""
        self._ensure_dir()
        with self._open_file(self.storage_path, "w") as f:
            json.dump([user.to_dict() for user in users], f, indent=2)

    def add(self, user: User) -> User:
        """Add a new user and persist.

        Args:
            user: The user to add.

        Returns:
            The added user with its ID set.
        """
        users = self.load()
        # Check for duplicate username
        for existing in users:
            if existing.username == user.username:
                raise StorageError(f"Username '{user.username}' already exists")
        users.append(user)
        self.save(users)
        return user

    def get(self, username: str) -> Optional[User]:
        """Find a user by username.

        Args:
            username: The username to find.

        Returns:
            The User if found, None otherwise.
        """
        for user in self.load():
            if user.username == username:
                return user
        return None

    def get_by_id(self, user_id: str) -> Optional[User]:
        """Find a user by ID.

        Args:
            user_id: The user ID to find.

        Returns:
            The User if found, None otherwise.
        """
        for user in self.load():
            if user.id == user_id:
                return user
        return None

    def delete(self, username: str) -> bool:
        """Remove a user by username.

        Args:
            username: The username to delete.

        Returns:
            True if the user was found and deleted.
        """
        users = self.load()
        before = len(users)
        users = [u for u in users if u.username != username]
        if len(users) == before:
            return False
        self.save(users)
        return True

    def update_profile(
        self,
        user_id: str,
        display_name: Optional[str] = None,
        email: Optional[str] = None,
    ) -> bool:
        """Update the display name and/or email of a user.

        Args:
            user_id: The ID of the user to update.
            display_name: New display name, or None to leave unchanged.
            email: New email, or None to leave unchanged.

        Returns:
            True if the user was found and updated, False otherwise.
        """
        users = self.load()
        for user in users:
            if user.id == user_id:
                if display_name is not None:
                    user.display_name = display_name
                if email is not None:
                    user.email = email
                self.save(users)
                return True
        return False

    def update_password(
        self,
        user_id: str,
        current_password: str,
        new_password: str,
    ) -> bool:
        """Update the password of a user.

        Args:
            user_id: The ID of the user to update.
            current_password: The current password for verification.
            new_password: The new password to set.

        Returns:
            True if the user was found and the password was updated, False otherwise.

        Raises:
            StorageError: If the current password is incorrect.
        """
        from snekdo.auth import hash_password

        users = self.load()
        for user in users:
            if user.id == user_id:
                if not verify_password(current_password, user.password_hash):
                    raise StorageError("Current password is incorrect")
                user.password_hash = hash_password(new_password)
                self.save(users)
                return True
        return False

    def get_profile(self, user_id: str) -> Optional[User]:
        """Find a user by ID, returning the user without the password hash.

        Args:
            user_id: The user ID to find.

        Returns:
            The User if found, None otherwise.
        """
        user = self.get_by_id(user_id)
        if user is not None:
            # Return a copy without the password hash for profile displays
            return User(
                id=user.id,
                username=user.username,
                display_name=user.display_name,
                email=user.email,
                password_hash="",
                created_at=user.created_at,
            )
        return None
