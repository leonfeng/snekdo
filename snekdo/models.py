"""Todo model for the snekdo application."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
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
class Todo:
    """A single todo item."""

    id: str = ""
    title: str = ""
    description: str = ""
    due: Optional[str] = None
    completed: bool = False
    created_at: str = ""  # ISO 8601
    priority: str = "medium"

    def __post_init__(self):
        """Generate ID if not provided."""
        if not self.id:
            self.id = generate()

    def to_dict(self) -> dict:
        """Serialize to dict for JSON storage."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due": self.due,
            "completed": self.completed,
            "created_at": self.created_at,
            "priority": self.priority,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Todo":
        """Deserialize from a dict loaded from JSON."""
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            due=data.get("due"),
            completed=data.get("completed", False),
            created_at=data["created_at"],
            priority=data.get("priority", "medium"),
        )
