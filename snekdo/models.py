"""Todo and User models for the snekdo application."""

from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from enum import StrEnum

from nanoid import generate


class Status(StrEnum):
    """Enum for filtering todos by status."""

    ALL = "all"
    PENDING = "pending"
    COMPLETED = "completed"


class Priority(StrEnum):
    """Enum for todo priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @classmethod
    def valid_values(cls):
        """Return list of valid priority values."""
        return [e.value for e in cls]


class Repeat(StrEnum):
    """Enum for todo recurrence intervals."""

    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

    @classmethod
    def valid_values(cls):
        """Return list of valid repeat values."""
        return [e.value for e in cls]


def _shift_monthly(day: date, months: int) -> date:
    """Advance ``day`` by ``months`` calendar months, clamping the day.

    The target day-of-month is clamped to the last valid day of the target
    month when it does not exist (e.g. Jan 31 -> Feb 28).
    """
    month_index = day.month - 1 + months
    year = day.year + month_index // 12
    month = month_index % 12 + 1
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(day.day, last_day))


def next_due_date(due: str | None, repeat: str, now: datetime | None = None) -> str:
    """Compute the next due date for a recurring todo.

    Args:
        due: The completed todo's due date as ``YYYY-MM-DD``, or ``None``.
        repeat: One of ``"daily"``, ``"weekly"``, ``"monthly"``, ``"yearly"``.
        now: Reference "today" for advancing past-due recurrences. Defaults to
            the current time; inject a fixed value for deterministic tests.

    Returns:
        The next due date as a ``YYYY-MM-DD`` string, guaranteed to be on or
        after today's date.

    Raises:
        ValueError: If ``repeat`` is not a supported recurrence interval.
    """
    if now is None:
        now = datetime.now()
    today = now.date()

    if repeat == "daily":
        base = date.fromisoformat(due) if due else today
        candidate = base + timedelta(days=1)
        while candidate < today:
            candidate += timedelta(days=1)
        return candidate.isoformat()

    if repeat == "weekly":
        base = date.fromisoformat(due) if due else today
        candidate = base + timedelta(days=7)
        while candidate < today:
            candidate += timedelta(days=7)
        return candidate.isoformat()

    if repeat == "monthly":
        base = date.fromisoformat(due) if due else today
        candidate = _shift_monthly(base, 1)
        while candidate < today:
            candidate = _shift_monthly(candidate, 1)
        return candidate.isoformat()

    if repeat == "yearly":
        base = date.fromisoformat(due) if due else today
        candidate = _shift_monthly(base, 12)
        while candidate < today:
            candidate = _shift_monthly(candidate, 12)
        return candidate.isoformat()

    raise ValueError(f"Invalid repeat value: {repeat!r}")


@dataclass
class User:
    """A user account."""

    id: str = ""
    username: str = ""
    display_name: str = ""
    email: str = ""
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
            "display_name": self.display_name,
            "email": self.email,
            "password_hash": self.password_hash,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> User:
        """Deserialize from a dict loaded from JSON."""
        return cls(
            id=data.get("id", ""),
            username=data.get("username", ""),
            display_name=data.get("display_name", ""),
            email=data.get("email", ""),
            password_hash=data.get("password_hash", ""),
            created_at=data.get("created_at", ""),
        )


@dataclass
class Todo:
    """A single todo item."""

    id: str = ""
    title: str = ""
    description: str = ""
    due: str | None = None  # YYYY-MM-DD, nullable
    completed: bool = False
    created_at: str = ""  # ISO 8601 timestamp
    priority: str = "medium"  # low | medium | high
    user_id: str | None = None
    repeat: str = Repeat.NONE.value
    last_completed_at: str | None = None

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
            "user_id": self.user_id,
            "repeat": self.repeat,
            "last_completed_at": self.last_completed_at,
        }
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Todo":
        """Deserialize from a dict (loaded from JSON)."""
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            due=data.get("due") or None,
            completed=data.get("completed", False),
            created_at=data.get("created_at", ""),
            priority=data.get("priority", "medium"),
            user_id=data.get("user_id") or None,
            repeat=data.get("repeat", Repeat.NONE.value),
            last_completed_at=data.get("last_completed_at") or None,
        )
