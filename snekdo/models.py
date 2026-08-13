"""Todo model for the snekdo application."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class Status(str, Enum):
    """Enum for filtering todos by status."""

    ALL = "all"
    PENDING = "pending"
    COMPLETED = "completed"


@dataclass
class Todo:
    """A single todo item."""

    id: str
    title: str
    description: str
    due: Optional[str]
    completed: bool
    created_at: str  # ISO 8601

    def to_dict(self) -> dict:
        """Serialize to dict for JSON storage."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due": self.due,
            "completed": self.completed,
            "created_at": self.created_at,
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
        )
