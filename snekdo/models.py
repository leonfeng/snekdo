"""Todo and User models for the snekdo application."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from nanoid import generate


class Status(str, Enum):
    """Enum for filtering todos by status."""

    ALL = "all"
    PENDING = "pending"
    COMPLETED = "completed"


class Priority(str, Enum):
    """Enum for todo priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @classmethod
    def valid_values(cls):
        """Return list of valid priority values."""
        return [e.value for e in cls]


@dataclass
class User:
    """A user account."""

    id: str = ""
    username: str = ""
    password_hash: str = ""
    created_at: str = ""  # ISO 8601

    def __post_init__(self):
        """Generate ID if not provided."""
        if not self.id:
            self.id = generate()

    def to_dict(self) -> dict:
        """Serialize to dict for JSON storage."""
        return {
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Deserialize from a dict loaded from JSON."""
        return cls(
            id=data.get("id", ""),
            username=data.get("username", ""),
            password_hash=data.get("password_hash", ""),
            created_at=data.get("created_at", ""),
        )


@dataclass
class Todo:
    """A single todo item."""

    id: str = ""
    title: str = ""
    description: str = ""
    due: Optional[str] = None
    completed: bool = False
    created_at: str = ""  # ISO 8601
    priority: str = "medium"
    user_id: Optional[str] = None

    def __post_init__(self):
        """Generate ID if not provided."""
        if not self.id:
            self.id = generate()

    def to_dict(self) -> dict:
        """Serialize to dict for JSON storage."""
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due": self.due,
            "completed": self.completed,
            "created_at": self.created_at,
            "priority": self.priority,
        }
        if self.user_id is not None:
            data["user_id"] = self.user_id
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Todo":
        """Deserialize from a dict loaded from JSON."""
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            due=data.get("due"),
            completed=data.get("completed", False),
            created_at=data.get("created_at", ""),
            priority=data.get("priority", "medium"),
            user_id=data.get("user_id"),
        )
