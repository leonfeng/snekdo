"""CLI entry point for the snekdo application."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from snekdo.api import create_app
from snekdo.api_client import ConnectionError, ServerHttpClient, ServerError, SyncSummary
from snekdo.web import register_web_routes
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

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start the FastAPI server")
    serve_parser.add_argument("--host", default="127.0.0.1", help="Host to bind the server")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to bind the server")
    serve_parser.add_argument("--storage", help="Path to the storage file", default=argparse.SUPPRESS)

    # Sync command
    sync_parser = subparsers.add_parser("sync", help="Synchronize with the FastAPI server")
    sync_parser.add_argument("--server", default="http://127.0.0.1:8000", help="Server base URL")
    sync_parser.add_argument("--direction", choices=["pull", "push", "both"], default="both", help="Sync direction")
    sync_parser.add_argument("--storage", help="Path to the storage file", default=argparse.SUPPRESS)

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
        elif args.command == "serve":
            return handle_serve(args, parser)
        elif args.command == "sync":
            return handle_sync(args, parser)
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

    # Compute dynamic ID column width based on the longest ID (capped at 35).
    max_id_width = 35
    id_width = min(max((len(t.id) for t in todos), default=5), max_id_width)
    # Ensure the column is at least as wide as the header text.
    id_width = max(id_width, len("ID"))

    # Fixed column widths for Status, Priority, Due, and Created At.
    status_width = 10
    priority_width = 10
    due_width = 15
    created_at_width = 25

    # Use a single space separator between all columns for uniform whitespace.
    sep = " "

    header = (
        f"{'ID':<{id_width}}{sep}{'Title':<{title_width}}{sep}"
        f"{'Status':<{status_width}}{sep}{'Priority':<{priority_width}}{sep}"
        f"{'Due':<{due_width}}{sep}{'Created At':<{created_at_width}}"
    )
    print(header)
    print("-" * len(header))
    for todo in todos:
        status = "✓" if todo.completed else "pending"
        due = todo.due if todo.due else ""
        created_at = todo.created_at if todo.created_at else ""
        title = _truncate_title(todo.title, title_width)
        id_ = _truncate_title(todo.id, id_width)
        print(
            f"{id_:<{id_width}}{sep}{title:<{title_width}}{sep}"
            f"{status:<{status_width}}{sep}{todo.priority:<{priority_width}}{sep}"
            f"{due:<{due_width}}{sep}{created_at:<{created_at_width}}"
        )

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


def handle_serve(args, parser) -> int:
    """Handle the serve command by starting the FastAPI server."""
    try:
        import uvicorn
    except ImportError:
        print("Error: uvicorn is not installed. Install with: pip install uvicorn", file=sys.stderr)
        return 1

    storage_path = _get_storage_path(args)
    app = create_app(storage_path=str(storage_path))
    register_web_routes(app, storage_path=str(storage_path))
    print(f"Starting snekdo server on {args.host}:{args.port}")
    print(f"Storage: {storage_path}")
    print(f"OpenAPI docs: http://{args.host}:{args.port}/docs")
    print(f"Web UI: http://{args.host}:{args.port}/")
    uvicorn.run(app, host=args.host, port=args.port)
    return 0


def handle_sync(args, parser) -> int:
    """Handle the sync command to synchronize with the FastAPI server."""
    

    storage_path = _get_storage_path(args)
    client = ServerHttpClient(base_url=args.server)

    try:
        summary = _sync(client, storage_path, args.direction)
        print(summary)
        if summary.errors:
            for error in summary.errors:
                print(f"Error: {error}", file=sys.stderr)
            return 1
        return 0
    except ConnectionError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ServerError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def _sync(client: ServerHttpClient, storage_path: Path, direction: str) -> SyncSummary:
    """Synchronize local storage with the server.

    Args:
        client: The HTTP client.
        storage_path: Path to the local storage file.
        direction: One of 'pull', 'push', or 'both'.

    Returns:
        A SyncSummary with counts of operations performed.
    """
    from snekdo.models import Todo
    from snekdo.storage import TodoStorage

    storage = TodoStorage(storage_path=str(storage_path))
    summary = SyncSummary()
    errors: list[str] = []

    try:
        server_todos = client.get_todos()
    except (ConnectionError, ServerError) as e:
        errors.append(f"Failed to fetch todos from server: {e}")
        summary.errors = errors
        return summary

    server_todo_map = {todo["id"]: todo for todo in server_todos}
    local_todos = storage.load()
    local_todo_map = {todo.id: todo for todo in local_todos}

    if direction in ("pull", "both"):
        # Pull: server is source of truth
        summary.pulled = len(server_todos)
        storage.save([Todo.from_dict(todo) for todo in server_todos])

    if direction in ("push", "both"):
        # Push: local is source of truth for local todos
        for local_todo in local_todos:
            server_data = server_todo_map.get(local_todo.id)
            if server_data is None:
                # Create new todo on server
                try:
                    client.create_todo(
                        title=local_todo.title,
                        description=local_todo.description,
                        due=local_todo.due or None,
                        priority=local_todo.priority,
                    )
                    summary.pushed += 1
                except (ConnectionError, ServerError) as e:
                    errors.append(f"Failed to create todo {local_todo.id}: {e}")
            else:
                # Update existing todo on server (local wins)
                try:
                    client.update_todo(
                        todo_id=local_todo.id,
                        title=local_todo.title,
                        description=local_todo.description,
                        due=local_todo.due or None,
                        priority=local_todo.priority,
                    )
                    summary.updated += 1
                except (ConnectionError, ServerError) as e:
                    errors.append(f"Failed to update todo {local_todo.id}: {e}")

    # Delete server todos that no longer exist locally (only on push/both)
    if direction in ("push", "both"):
        for server_id in server_todo_map:
            if server_id not in local_todo_map:
                try:
                    client.delete_todo(server_id)
                    summary.deleted += 1
                except (ConnectionError, ServerError) as e:
                    errors.append(f"Failed to delete todo {server_id}: {e}")

    if errors:
        summary.errors = errors

    return summary


if __name__ == "__main__":
    sys.exit(main())
