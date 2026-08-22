"""SQLite storage backend for snekdo todos."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from snekdo.models import Todo, User, Priority

logger = logging.getLogger(__name__)


class TodoStorageSQLite:
    """SQLite-backed storage for todo items."""

    def __init__(self, database_path: str | None = None) -> None:
        if database_path is not None:
            self.database_path = Path(database_path)
        else:
            self.database_path = Path.home() / ".snekdo" / "todos.db"

        self._ensure_dir()
        self._init_db()

    def _ensure_dir(self) -> None:
        """Create the storage directory if it does not exist."""
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

    def _init_db(self) -> None:
        """Initialize the SQLite database and create tables if needed."""
        conn = self._get_connection()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    due TEXT,
                    completed INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL,
                    priority TEXT NOT NULL DEFAULT 'medium',
                    user_id TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    display_name TEXT,
                    email TEXT,
                    password_hash TEXT,
                    created_at TEXT NOT NULL
                )
            """)
            conn.commit()
        finally:
            conn.close()

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection with proper settings."""
        conn = sqlite3.connect(str(self.database_path))
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        return conn

    def _todo_from_row(self, row: tuple) -> Todo:
        """Convert a database row to a Todo model instance."""
        return Todo(
            id=row[0],
            title=row[1],
            description=row[2],
            due=row[3] if row[3] else None,
            completed=bool(row[4]),
            created_at=row[5],
            priority=Priority(row[6]) if row[6] else Priority.MEDIUM,
            user_id=row[7],
        )

    def _row_to_dict(self, row: tuple) -> dict:
        """Convert a database row to a dict for serialization."""
        return {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "due": row[3],
            "completed": bool(row[4]),
            "created_at": row[5],
            "priority": row[6],
            "user_id": row[7],
        }

    def load(self, user_id: str | None = None) -> list[Todo]:
        """Load all todos from the SQLite database.

        Args:
            user_id: If provided, filter todos to only those belonging to this user.

        Returns:
            A list of Todo instances.
        """
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                "SELECT id, title, description, due, completed, created_at, priority, user_id FROM todos"
            )
            if user_id is not None:
                cursor = cursor.execute(
                    "SELECT id, title, description, due, completed, created_at, priority, user_id FROM todos WHERE user_id = ?",
                    (user_id,),
                )
            rows = cursor.fetchall()
            return [self._todo_from_row(row) for row in rows]
        finally:
            conn.close()

    def save(self, todos: list[Todo]) -> None:
        """Save all todos to the SQLite database."""
        conn = self._get_connection()
        try:
            for todo in todos:
                conn.execute(
                    """INSERT OR REPLACE INTO todos (id, title, description, due, completed, created_at, priority, user_id)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        todo.id,
                        todo.title,
                        todo.description,
                        todo.due,
                        1 if todo.completed else 0,
                        todo.created_at,
                        todo.priority.value,
                        todo.user_id,
                    ),
                )
            conn.commit()
        finally:
            conn.close()

    def add(self, todo: Todo) -> None:
        """Append a todo and persist."""
        todos = self.load()
        todos.append(todo)
        self.save(todos)

    def get(self, todo_id: str, user_id: str | None = None) -> Todo | None:
        """Find a todo by ID.

        Args:
            todo_id: The ID of the todo to find.
            user_id: If provided, also filter by user.

        Returns:
            The Todo if found, None otherwise.
        """
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                "SELECT id, title, description, due, completed, created_at, priority, user_id FROM todos WHERE id = ?",
                (todo_id,),
            )
            if user_id is not None:
                cursor = cursor.execute(
                    "SELECT id, title, description, due, completed, created_at, priority, user_id FROM todos WHERE id = ? AND user_id = ?",
                    (todo_id, user_id),
                )
            row = cursor.fetchone()
            if row is None:
                return None
            return self._todo_from_row(row)
        finally:
            conn.close()

    def delete(self, todo_id: str, user_id: str | None = None) -> bool:
        """Remove a todo by ID.

        Args:
            todo_id: The ID of the todo to delete.
            user_id: If provided, also filter by user.

        Returns:
            True if the todo was found and deleted.
        """
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                "SELECT id FROM todos WHERE id = ?",
                (todo_id,),
            )
            if user_id is not None:
                cursor = cursor.execute(
                    "SELECT id FROM todos WHERE id = ? AND user_id = ?",
                    (todo_id, user_id),
                )
            row = cursor.fetchone()
            if row is None:
                return False
            conn.execute(
                "DELETE FROM todos WHERE id = ?",
                (todo_id,) if user_id is None else (todo_id, user_id),
            )
            conn.commit()
            return True
        finally:
            conn.close()

    def complete(self, todo_id: str, user_id: str | None = None) -> bool:
        """Mark a todo as complete by ID.

        Args:
            todo_id: The ID of the todo to complete.
            user_id: If provided, also filter by user.

        Returns:
            True if the todo was found and updated.
        """
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                "SELECT id FROM todos WHERE id = ?",
                (todo_id,),
            )
            if user_id is not None:
                cursor = cursor.execute(
                    "SELECT id FROM todos WHERE id = ? AND user_id = ?",
                    (todo_id, user_id),
                )
            row = cursor.fetchone()
            if row is None:
                return False
            conn.execute(
                "UPDATE todos SET completed = 1 WHERE id = ?",
                (todo_id,) if user_id is None else (todo_id, user_id),
            )
            conn.commit()
            return True
        finally:
            conn.close()

    def modify(self, todo_id: str, user_id: str | None = None, **kwargs) -> bool:
        """Modify an existing todo by ID.

        Args:
            todo_id: The ID of the todo to modify.
            user_id: If provided, also filter by user.
            **kwargs: Fields to update (title, description, due, priority, completed).

        Returns:
            True if the todo was found and updated, False otherwise.
        """
        conn = self._get_connection()
        try:
            # Check if todo exists
            cursor = conn.execute(
                "SELECT id FROM todos WHERE id = ?",
                (todo_id,),
            )
            if user_id is not None:
                cursor = cursor.execute(
                    "SELECT id FROM todos WHERE id = ? AND user_id = ?",
                    (todo_id, user_id),
                )
            row = cursor.fetchone()
            if row is None:
                return False

            # Build update query dynamically
            update_fields = []
            update_values = []

            if "title" in kwargs:
                update_fields.append("title = ?")
                update_values.append(kwargs["title"])
            if "description" in kwargs:
                update_fields.append("description = ?")
                update_values.append(kwargs["description"])
            if "due" in kwargs:
                update_fields.append("due = ?")
                update_values.append(kwargs["due"])
            if "priority" in kwargs:
                update_fields.append("priority = ?")
                update_values.append(kwargs["priority"].value if hasattr(kwargs["priority"], "value") else kwargs["priority"])
            if "completed" in kwargs:
                update_fields.append("completed = ?")
                update_values.append(1 if kwargs["completed"] else 0)

            if not update_fields:
                return True

            update_values.append(todo_id)
            if user_id is not None:
                query = f"UPDATE todos SET {', '.join(update_fields)} WHERE id = ? AND user_id = ?"
                conn.execute(query, *update_values, user_id)
            else:
                query = f"UPDATE todos SET {', '.join(update_fields)} WHERE id = ?"
                conn.execute(query, update_values)

            conn.commit()
            return True
        finally:
            conn.close()


class UserStorageSQLite:
    """SQLite-backed storage for user accounts."""

    def __init__(self, database_path: str | None = None) -> None:
        if database_path is not None:
            self.database_path = Path(database_path)
        else:
            self.database_path = Path.home() / ".snekdo" / "users.db"

        self._ensure_dir()
        self._init_db()

    def _ensure_dir(self) -> None:
        """Create the storage directory if it does not exist."""
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

    def _init_db(self) -> None:
        """Initialize the SQLite database and create tables if needed."""
        conn = self._get_connection()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    display_name TEXT,
                    email TEXT,
                    password_hash TEXT,
                    created_at TEXT NOT NULL
                )
            """)
            conn.commit()
        finally:
            conn.close()

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection with proper settings."""
        conn = sqlite3.connect(str(self.database_path))
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        return conn

    def _user_from_row(self, row: tuple) -> User:
        """Convert a database row to a User model instance."""
        return User(
            id="",
            username=row[0],
            display_name=row[1],
            email=row[2],
            password_hash=row[3],
            created_at=row[4],
        )

    def load(self) -> list[User]:
        """Load all users from the SQLite database."""
        conn = self._get_connection()
        try:
            cursor = conn.execute("SELECT username, display_name, email, password_hash, created_at FROM users")
            rows = cursor.fetchall()
            return [self._user_from_row(row) for row in rows]
        finally:
            conn.close()

    def save(self, user: User) -> User:
        """Save a user to the SQLite database."""
        conn = self._get_connection()
        try:
            conn.execute(
                """INSERT OR REPLACE INTO users (username, display_name, email, password_hash, created_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    user.username,
                    user.display_name,
                    user.email,
                    user.password_hash,
                    user.created_at,
                ),
            )
            conn.commit()
            return user
        finally:
            conn.close()

    def add(self, user: User) -> User:
        """Add a new user and persist."""
        users = self.load()
        for existing in users:
            if existing.username == user.username:
                raise StorageError(f"Username '{user.username}' already exists")
        users.append(user)
        self.save(user)
        return user

    def get(self, username: str) -> User | None:
        """Find a user by username.

        Args:
            username: The username to find.

        Returns:
            The User if found, None otherwise.
        """
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                "SELECT username, display_name, email, password_hash, created_at FROM users WHERE username = ?",
                (username,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return self._user_from_row(row)
        finally:
            conn.close()

    def get_by_id(self, user_id: str) -> User | None:
        """Find a user by ID (uses username as primary key in this implementation).

        Args:
            user_id: The user ID to find.

        Returns:
            The User if found, None otherwise.
        """
        return self.get(user_id)

    def delete(self, username: str) -> bool:
        """Remove a user by username.

        Args:
            username: The username to delete.

        Returns:
            True if the user was found and deleted.
        """
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                "SELECT username FROM users WHERE username = ?",
                (username,),
            )
            row = cursor.fetchone()
            if row is None:
                return False
            conn.execute(
                "DELETE FROM users WHERE username = ?",
                (username,),
            )
            conn.commit()
            return True
        finally:
            conn.close()

    def delete_user_with_todos(
        self, user_id: str, todo_storage: TodoStorageSQLite
    ) -> bool:
        """Remove a user by ID and all their todos in a single operation.

        Args:
            user_id: The ID of the user to delete.
            todo_storage: The TodoStorageSQLite instance to use for removing the user's todos.

        Returns:
            True if the user was found and deleted, False otherwise.
        """
        todo_storage.delete_all_user_todos(user_id)
        return self.delete(user_id)

    def update_profile(
        self,
        user_id: str,
        display_name: str | None = None,
        email: str | None = None,
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
                self.save(user)
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
        """
        from snekdo.auth import verify_password, hash_password

        users = self.load()
        for user in users:
            if user.id == user_id:
                if not verify_password(current_password, user.password_hash):
                    raise StorageError("Current password is incorrect")
                user.password_hash = hash_password(new_password)
                self.save(user)
                return True
        return False

    def get_profile(self, user_id: str) -> User | None:
        """Find a user by ID, returning the user without the password hash.

        Args:
            user_id: The user ID to find.

        Returns:
            The User if found, None otherwise.
        """
        user = self.get_by_id(user_id)
        if user is not None:
            return User(
                id=user.id,
                username=user.username,
                display_name=user.display_name,
                email=user.email,
                password_hash="",
                created_at=user.created_at,
            )
        return None