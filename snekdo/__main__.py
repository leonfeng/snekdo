"""CLI entry point for the snekdo application."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from snekdo.models import Todo
from snekdo.storage import StorageError, TodoStorage


def validate_due_date(due_date: str) -> str:
    """Validate a due date string.

    Args:
        due_date: The due date string to validate (YYYY-MM-DD format).

    Returns:
        The validated due date string.

    Raises:
        ValueError: If the date format is invalid or the date is in the past.
    """
    if due_date is None or due_date.strip() == "":
        return ""
    try:
        parsed = datetime.strptime(due_date, "%Y-%m-%d")
        if parsed.date() < datetime.now().date():
            raise ValueError(f"Due date '{due_date}' cannot be in the past")
        return due_date
    except ValueError:
        raise ValueError(f"Invalid due date format: '{due_date}'. Use YYYY-MM-DD format and a future date")


def _parse_created_at(created_at: str) -> datetime:
    """Parse a created_at ISO 8601 string into a datetime object.

    Empty or missing values are treated as the earliest possible date (epoch).
    Malformed strings are also treated as the earliest possible date.
    """
    if not created_at:
        return datetime.min
    try:
        return datetime.fromisoformat(created_at)
    except (ValueError, TypeError):
        return datetime.min

def _truncate_title(title: str, max_width: int) -> str:
    """Truncate a title to fit within max_width, appending an ellipsis.

    If the title fits within max_width, it is returned unchanged.
    Otherwise, the title is truncated to max_width - 3 characters and
    '...' is appended.
    """
    if len(title) <= max_width:
        return title
    return title[: max_width - 3] + "..."



def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="snekdo",
        description="A simple CLI todo list manager",
    )
    parser.add_argument("--storage", help="Path to the storage file", default=argparse.SUPPRESS)
    parser.add_argument("--debug", action="store_true", help="Print debug information")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new todo item")
    add_parser.add_argument("--title", required=True, help="Title of the todo")
    add_parser.add_argument("--description", default="", help="Description of the todo")
    add_parser.add_argument("--due", help="Due date (e.g., 2024-12-31)")
    add_parser.add_argument("--priority", default="medium", choices=["low", "medium", "high"], help="Priority level (low, medium, high)")
    add_parser.add_argument("--storage", help="Path to the storage file", default=argparse.SUPPRESS)

    # List command
    list_parser = subparsers.add_parser("list", help="List all todo items")
    list_parser.add_argument("--status", choices=["all", "pending", "completed"], default="pending")
    list_parser.add_argument("--limit", type=int, help="Limit the number of results")
    list_parser.add_argument("--priority", default=None, choices=["low", "medium", "high"], help="Filter by priority level")
    list_parser.add_argument("--sort", default="created_at", choices=["created_at", "title", "priority", "completed"], help="Sort by field (created_at, title, priority, completed)")
    list_parser.add_argument("--reverse", action="store_true", default=False, dest="reverse", help="Reverse the sort order")
    list_parser.add_argument("--storage", help="Path to the storage file", default=argparse.SUPPRESS)

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a todo as complete")
    complete_parser.add_argument("todo_id", help="ID of the todo to complete")
    complete_parser.add_argument("--storage", help="Path to the storage file", default=argparse.SUPPRESS)

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a todo")
    delete_parser.add_argument("todo_id", help="ID of the todo to delete")
    delete_parser.add_argument("--storage", help="Path to the storage file", default=argparse.SUPPRESS)

    # Modify command
    modify_parser = subparsers.add_parser("modify", help="Modify an existing todo")
    modify_parser.add_argument("todo_id", help="ID of the todo to modify")
    modify_parser.add_argument("--title", help="New title for the todo")
    modify_parser.add_argument("--description", default=None, help="New description for the todo")
    modify_parser.add_argument("--due", help="New due date for the todo (e.g., 2024-12-31)")
    modify_parser.add_argument("--priority", default=None, choices=["low", "medium", "high"], help="New priority level")
    modify_parser.add_argument("--storage", help="Path to the storage file", default=argparse.SUPPRESS)

    # Show command
    show_parser = subparsers.add_parser("show", help="Show details of a todo item")
    show_parser.add_argument("todo_id", help="ID of the todo to show")
    show_parser.add_argument("--storage", help="Path to the storage file", default=argparse.SUPPRESS)

    return parser


def _get_storage_path(args) -> Path:
    """Return the effective storage path from the parsed args.

    Uses ``args.storage`` if provided (and not ``argparse.SUPPRESS``),
    otherwise falls back to the default ``~/.snekdo/todos.json``.
    """
    storage = getattr(args, "storage", None)
    if storage is not None and storage is not argparse.SUPPRESS:
        return Path(storage)
    return Path.home() / ".snekdo" / "todos.json"


def main() -> int:
    """Main entry point for the CLI."""
    parser = create_parser()

    try:
        args = parser.parse_args()
        return handle_command(args, parser)
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 1


def handle_command(args, parser) -> int:
    """Handle the parsed command line arguments."""
    if getattr(args, "debug", False):
        storage_path = _get_storage_path(args)
        command = getattr(args, "command", None) or "unknown"
        print(f"DEBUG: command={command}", file=sys.stderr)
        print(f"DEBUG: storage_path={storage_path}", file=sys.stderr)
    try:
        if args.command == "add":
            return handle_add(args, parser)
        elif args.command == "list":
            return handle_list(args, parser)
        elif args.command == "complete":
            return handle_complete(args, parser)
        elif args.command == "delete":
            return handle_delete(args, parser)
        elif args.command == "modify":
            return handle_modify(args, parser)
        elif args.command == "show":
            return handle_show(args, parser)
        else:
            parser.print_help()
            return 0
    except StorageError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_add(args, parser) -> int:
    """Handle the add command."""
    storage = TodoStorage(storage_path=getattr(args, "storage", None))
    try:
        due = validate_due_date(args.due) if args.due else ""
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    todo = Todo(
        title=args.title,
        description=args.description,
        due=due,
        completed=False,
        created_at=datetime.now().isoformat(),
        priority=args.priority,
    )
    storage.add(todo)
    print(f"Added todo: {todo.title}")
    return 0


def handle_list(args, parser) -> int:
    """Handle the list command."""
    storage = TodoStorage(storage_path=getattr(args, "storage", None))
    todos = storage.load()

    # Filter by status
    if args.status == "pending":
        todos = [t for t in todos if not t.completed]
    elif args.status == "completed":
        todos = [t for t in todos if t.completed]

    # Filter by priority
    if args.priority:
        todos = [t for t in todos if t.priority == args.priority]

    # Validate the sort field
    sort_key = args.sort
    valid_sort_fields = {"created_at", "title", "priority", "completed"}
    if sort_key not in valid_sort_fields:
        print(f"Error: Invalid sort field '{sort_key}'. Valid sort fields are: created_at, title, priority, completed", file=sys.stderr)
        return 1

    # Sort by the specified field
    if sort_key == "created_at":
        todos = sorted(todos, key=lambda x: _parse_created_at(x.created_at), reverse=args.reverse)
    elif sort_key == "title":
        todos = sorted(todos, key=lambda x: x.title.lower(), reverse=args.reverse)
    elif sort_key == "priority":
        priority_order = {"high": 0, "medium": 1, "low": 2}
        todos = sorted(todos, key=lambda x: priority_order.get(x.priority, 1), reverse=args.reverse)
    elif sort_key == "completed":
        todos = sorted(todos, key=lambda x: x.completed, reverse=args.reverse)

    # Limit results
    if args.limit:
        todos = todos[:args.limit]

    if not todos:
        print("No todos found.")
        return 0

    # Compute dynamic Title column width based on the longest title (capped at 40).
    max_title_width = 40
    title_width = min(max((len(t.title) for t in todos), default=5), max_title_width)
    # Ensure the column is at least as wide as the header text.
    title_width = max(title_width, len("Title"))

    header = f"{'ID':<35} {'Title':<{title_width}} {'Status':<10} {'Priority':<10} {'Due':<15} {'Created At':<25}"
    print(header)
    print("-" * len(header))
    for todo in todos:
        status = "✓" if todo.completed else "pending"
        due = todo.due if todo.due else ""
        created_at = todo.created_at if todo.created_at else ""
        title = _truncate_title(todo.title, title_width)
        print(f"{todo.id:<35} {title:<{title_width}} {status:<10} {todo.priority:<10} {due:<15} {created_at:<25}")

    return 0


def handle_complete(args, parser) -> int:
    """Handle the complete command."""
    storage = TodoStorage(storage_path=getattr(args, "storage", None))
    todo = storage.get(args.todo_id)
    if todo is None:
        print(f"Error: Todo with ID {args.todo_id} not found")
        return 1
    storage.complete(args.todo_id)
    print(f"Completed todo: {todo.title}")
    return 0


def handle_delete(args, parser) -> int:
    """Handle the delete command."""
    storage = TodoStorage(storage_path=getattr(args, "storage", None))
    todo = storage.get(args.todo_id)
    if todo is None:
        print(f"Error: Todo with ID {args.todo_id} not found")
        return 1
    storage.delete(args.todo_id)
    print(f"Deleted todo: {todo.title}")
    return 0


def handle_modify(args, parser) -> int:
    """Handle the modify command."""
    # Validate that at least one field is being updated
    if args.title is None and args.description is None and args.due is None and args.priority is None:
        print("Error: No fields to update. Use --title, --description, --due, or --priority to specify fields to update.")
        return 1

    storage = TodoStorage(storage_path=getattr(args, "storage", None))
    todo = storage.get(args.todo_id)
    if todo is None:
        print(f"Error: Todo with ID {args.todo_id} not found")
        return 1

    # Build update dict with only provided fields
    update_data = {}
    if args.title is not None:
        update_data["title"] = args.title
    if args.description is not None:
        update_data["description"] = args.description
    if args.due is not None:
        try:
            update_data["due"] = validate_due_date(args.due)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    if args.priority is not None:
        update_data["priority"] = args.priority

    storage.modify(args.todo_id, **update_data)
    print(f"Updated todo: {todo.title}")
    return 0


def handle_show(args, parser) -> int:
    """Handle the show command."""
    storage = TodoStorage(storage_path=getattr(args, "storage", None))
    todo = storage.get(args.todo_id)
    if todo is None:
        print(f"Error: Todo with ID {args.todo_id} not found")
        return 1

    status = "✓" if todo.completed else "pending"
    due = todo.due if todo.due else ""
    created_at = todo.created_at if todo.created_at else ""

    print(f"ID: {todo.id}")
    print(f"Title: {todo.title}")
    print(f"Description: {todo.description}")
    print(f"Due: {due}")
    print(f"Priority: {todo.priority}")
    print(f"Status: {status}")
    print(f"Created At: {created_at}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
