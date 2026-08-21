"""Shared due-date validation utilities."""

from datetime import datetime


def validate_due_date(due_date: str) -> str | None:
    """Validate a due date string.

    Args:
        due_date: The due date string to validate (YYYY-MM-DD format).

    Returns:
        The validated due date string, or ``None`` if the input is empty or
        ``None``.

    Raises:
        ValueError: If the date format is invalid or the date is in the past.
    """
    if due_date is None or due_date.strip() == "":
        return None
    try:
        parsed = datetime.strptime(due_date, "%Y-%m-%d")
        if parsed.date() < datetime.now().date():
            raise ValueError(f"Due date '{due_date}' cannot be in the past")
        return due_date
    except ValueError:
        raise ValueError(
            f"Invalid due date format: '{due_date}'. "
            f"Use YYYY-MM-DD format and a future date"
        )
