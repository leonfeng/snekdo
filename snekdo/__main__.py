"""CLI entry point for the snekdo application."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

from snekdo.api import create_app
from snekdo.api_client import (
    AuthenticationError,
    ConnectionError,
    ServerError,
    ServerHttpClient,
    SyncSummary,
)
from snekdo.due_date import validate_due_date
from snekdo.models import Todo
from snekdo.storage import StorageError, TodoStorage
from snekdo.web import register_web_routes

CREDENTIALS_PATH = Path.home() / ".snekdo" / "credentials.json"


def _get_credentials_path(storage_path: Path | None = None) -> Path:
    """Return the path to the credentials file.

    Uses the default ``~/.snekdo/credentials.json`` unless a custom
    storage path is provided, in which case the credentials are stored
    alongside the storage file.
    """
    if storage_path is not None:
        return storage_path.parent / ".snekdo_credentials.json"
    return CREDENTIALS_PATH


def _read_credentials(credentials_path: Path) -> dict | None:
    """Read the stored credentials from disk.

    Returns:
        The credentials dict with ``access_token`` and ``token_type``,
        or ``None`` if the file does not exist.
    """
    if not credentials_path.exists():
        return None
    with open(credentials_path) as f:
        return json.load(f)


def _write_credentials(
    credentials_path: Path, access_token: str, token_type: str = "bearer"
) -> None:
    """Write credentials to disk."""
    credentials_path.parent.mkdir(parents=True, exist_ok=True)
    with open(credentials_path, "w") as f:
        json.dump({"access_token": access_token, "token_type": token_type}, f, indent=2)


def _delete_credentials(credentials_path: Path) -> None:
    """Delete the credentials file."""
    if credentials_path.exists():
        credentials_path.unlink()


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
    parser.add_argument(
        "--storage", help="Path to the storage file", default=argparse.SUPPRESS
    )
    parser.add_argument("--debug", action="store_true", help="Print debug information")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new todo item")
    add_parser.add_argument("--title", required=True, help="Title of the todo")
    add_parser.add_argument("--description", default="", help="Description of the todo")
    add_parser.add_argument("--due", help="Due date (e.g., 2024-12-31)")
    add_parser.add_argument(
        "--priority",
        default="medium",
        choices=["low", "medium", "high"],
        help="Priority level (low, medium, high)",
    )
    add_parser.add_argument(
        "--repeat",
        default="none",
        choices=["none", "daily", "weekly", "monthly", "yearly"],
        help="Recurrence interval (none, daily, weekly, monthly, yearly)",
    )
    add_parser.add_argument(
        "--storage", help="Path to the storage file", default=argparse.SUPPRESS
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List all todo items")
    list_parser.add_argument(
        "--status", choices=["all", "pending", "completed"], default="pending"
    )
    list_parser.add_argument("--limit", type=int, help="Limit the number of results")
    list_parser.add_argument(
        "--priority",
        default=None,
        choices=["low", "medium", "high"],
        help="Filter by priority level",
    )
    list_parser.add_argument(
        "--sort",
        default="created_at",
        choices=["created_at", "title", "priority", "completed"],
        help="Sort by field (created_at, title, priority, completed)",
    )
    list_parser.add_argument(
        "--reverse",
        action="store_true",
        default=False,
        dest="reverse",
        help="Reverse the sort order",
    )
    list_parser.add_argument(
        "--storage", help="Path to the storage file", default=argparse.SUPPRESS
    )

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a todo as complete")
    complete_parser.add_argument("todo_id", help="ID of the todo to complete")
    complete_parser.add_argument(
        "--storage", help="Path to the storage file", default=argparse.SUPPRESS
    )

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a todo")
    delete_parser.add_argument("todo_id", help="ID of the todo to delete")
    delete_parser.add_argument(
        "--storage", help="Path to the storage file", default=argparse.SUPPRESS
    )

    # Modify command
    modify_parser = subparsers.add_parser("modify", help="Modify an existing todo")
    modify_parser.add_argument("todo_id", help="ID of the todo to modify")
    modify_parser.add_argument("--title", help="New title for the todo")
    modify_parser.add_argument(
        "--description", default=None, help="New description for the todo"
    )
    modify_parser.add_argument(
        "--due", help="New due date for the todo (e.g., 2024-12-31)"
    )
    modify_parser.add_argument(
        "--priority",
        default=None,
        choices=["low", "medium", "high"],
        help="New priority level",
    )
    modify_parser.add_argument(
        "--completed",
        type=str,
        default=None,
        choices=["true", "false"],
        help="Set the completed status (true or false)",
    )
    modify_parser.add_argument(
        "--storage", help="Path to the storage file", default=argparse.SUPPRESS
    )

    # Show command
    show_parser = subparsers.add_parser("show", help="Show details of a todo item")
    show_parser.add_argument("todo_id", help="ID of the todo to show")
    show_parser.add_argument(
        "--storage", help="Path to the storage file", default=argparse.SUPPRESS
    )

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start the FastAPI server")
    serve_parser.add_argument(
        "--host", default="127.0.0.1", help="Host to bind the server"
    )
    serve_parser.add_argument(
        "--port", type=int, default=8000, help="Port to bind the server"
    )
    serve_parser.add_argument(
        "--storage", help="Path to the storage file", default=argparse.SUPPRESS
    )

    # Sync command
    sync_parser = subparsers.add_parser(
        "sync", help="Synchronize with the FastAPI server"
    )
    sync_parser.add_argument(
        "--server", default="http://127.0.0.1:8000", help="Server base URL"
    )
    sync_parser.add_argument(
        "--direction",
        choices=["pull", "push", "both"],
        default="both",
        help="Sync direction",
    )
    sync_parser.add_argument(
        "--storage", help="Path to the storage file", default=argparse.SUPPRESS
    )

    # Register command
    register_parser = subparsers.add_parser("register", help="Register a new account")
    register_parser.add_argument(
        "--username", required=True, help="Username for the new account"
    )
    register_parser.add_argument(
        "--password", required=True, help="Password for the new account"
    )
    register_parser.add_argument(
        "--server", default="http://127.0.0.1:8000", help="Server base URL"
    )
    register_parser.add_argument(
        "--storage", help="Path to the storage file", default=argparse.SUPPRESS
    )

    # Login command
    login_parser = subparsers.add_parser("login", help="Log in to an existing account")
    login_parser.add_argument("--username", required=True, help="Username")
    login_parser.add_argument("--password", required=True, help="Password")
    login_parser.add_argument(
        "--server", default="http://127.0.0.1:8000", help="Server base URL"
    )
    login_parser.add_argument(
        "--storage", help="Path to the storage file", default=argparse.SUPPRESS
    )

    # Logout command
    logout_parser = subparsers.add_parser(
        "logout", help="Log out and remove stored credentials"
    )
    logout_parser.add_argument(
        "--storage", help="Path to the storage file", default=argparse.SUPPRESS
    )

    # Profile command
    profile_parser = subparsers.add_parser("profile", help="View your profile")
    profile_parser.add_argument(
        "--server", default="http://127.0.0.1:8000", help="Server base URL"
    )
    profile_parser.add_argument(
        "--storage", help="Path to the storage file", default=argparse.SUPPRESS
    )

    # Profile update command
    profile_update_parser = subparsers.add_parser(
        "profile-update", help="Update your profile"
    )
    profile_update_parser.add_argument(
        "--server", default="http://127.0.0.1:8000", help="Server base URL"
    )
    profile_update_parser.add_argument(
        "--display-name", default=None, help="New display name"
    )
    profile_update_parser.add_argument("--email", default=None, help="New email")
    profile_update_parser.add_argument(
        "--storage", help="Path to the storage file", default=argparse.SUPPRESS
    )

    # Change password command
    change_password_parser = subparsers.add_parser(
        "change-password", help="Change your password"
    )
    change_password_parser.add_argument(
        "--server", default="http://127.0.0.1:8000", help="Server base URL"
    )
    change_password_parser.add_argument(
        "--current-password", required=True, help="Current password"
    )
    change_password_parser.add_argument(
        "--new-password", required=True, help="New password"
    )
    change_password_parser.add_argument(
        "--confirm-password", required=True, help="Confirm new password"
    )
    change_password_parser.add_argument(
        "--storage", help="Path to the storage file", default=argparse.SUPPRESS
    )

    # Delete account command
    delete_account_parser = subparsers.add_parser(
        "delete-account", help="Delete your account on the server"
    )
    delete_account_parser.add_argument(
        "--server", default="http://127.0.0.1:8000", help="Server base URL"
    )
    delete_account_parser.add_argument(
        "--password", required=True, help="Your current password"
    )
    delete_account_parser.add_argument(
        "--storage", help="Path to the storage file", default=argparse.SUPPRESS
    )

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
        _stderr = logging.StreamHandler(sys.stderr)
        _stderr.setFormatter(logging.Formatter("DEBUG: %(message)s"))
        _logger = logging.getLogger(__name__)
        _logger.setLevel(logging.DEBUG)
        _logger.addHandler(_stderr)
        storage_path = _get_storage_path(args)
        command = getattr(args, "command", None) or "unknown"
        _logger.debug(f"command={command}")
        _logger.debug(f"storage_path={storage_path}")
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
        elif args.command == "register":
            return handle_register(args, parser)
        elif args.command == "login":
            return handle_login(args, parser)
        elif args.command == "logout":
            return handle_logout(args, parser)
        elif args.command == "profile":
            return handle_profile(args, parser)
        elif args.command == "profile-update":
            return handle_profile_update(args, parser)
        elif args.command == "change-password":
            return handle_change_password(args, parser)
        elif args.command == "delete-account":
            return handle_delete_account(args, parser)
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
        due = validate_due_date(args.due)
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
        repeat=getattr(args, "repeat", "none"),
    )
    storage.add(todo)
    repeat_info = f" (repeats {getattr(args, 'repeat', 'none')})" if getattr(args, "repeat", "none") != "none" else ""
    print(f"Added todo: {todo.title}{repeat_info}")
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
        print(
            f"Error: Invalid sort field '{sort_key}'. "
            f"Valid sort fields are: created_at, title, priority, completed",
            file=sys.stderr,
        )
        return 1

    # Sort by the specified field
    if sort_key == "created_at":
        todos = sorted(
            todos, key=lambda x: _parse_created_at(x.created_at), reverse=args.reverse
        )
    elif sort_key == "title":
        todos = sorted(todos, key=lambda x: x.title.lower(), reverse=args.reverse)
    elif sort_key == "priority":
        priority_order = {"high": 0, "medium": 1, "low": 2}
        todos = sorted(
            todos, key=lambda x: priority_order.get(x.priority, 1), reverse=args.reverse
        )
    elif sort_key == "completed":
        todos = sorted(todos, key=lambda x: x.completed, reverse=args.reverse)

    # Limit results
    if args.limit:
        todos = todos[: args.limit]

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
    repeat_width = 8
    created_at_width = 25

    # Use a single space separator between all columns for uniform whitespace.
    sep = " "

    header = (
        f"{'ID':<{id_width}}{sep}{'Title':<{title_width}}{sep}"
        f"{'Status':<{status_width}}{sep}{'Priority':<{priority_width}}{sep}"
        f"{'Due':<{due_width}}{sep}{'Repeat':<{repeat_width}}{sep}"
        f"{'Created At':<{created_at_width}}"
    )
    print(header)
    print("-" * len(header))
    for todo in todos:
        status = "✓" if todo.completed else "pending"
        due = todo.due if todo.due else ""
        created_at = todo.created_at if todo.created_at else ""
        repeat_tag = f"({todo.repeat})" if todo.repeat and todo.repeat != "none" else ""
        title = _truncate_title(todo.title, title_width)
        id_ = _truncate_title(todo.id, id_width)
        print(
            f"{id_:<{id_width}}{sep}{title:<{title_width}}{sep}"
            f"{status:<{status_width}}{sep}{todo.priority:<{priority_width}}{sep}"
            f"{due:<{due_width}}{sep}{repeat_tag:<{repeat_width}}{sep}"
            f"{created_at:<{created_at_width}}"
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
    if (
        args.title is None
        and args.description is None
        and args.due is None
        and args.priority is None
        and getattr(args, "completed", None) is None
    ):
        print(
            "Error: No fields to update. "
            "Use --title, --description, --due, "
            "--priority, or --completed to specify fields to update."
        )
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
    if args.due:
        try:
            update_data["due"] = validate_due_date(args.due)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    if args.priority is not None:
        update_data["priority"] = args.priority

    completed = getattr(args, "completed", None)
    if completed is not None:
        update_data["completed"] = completed.lower() == "true"

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
        print(
            "Error: uvicorn is not installed. Install with: pip install uvicorn",
            file=sys.stderr,
        )
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
    credentials_path = _get_credentials_path(storage_path)
    client = ServerHttpClient(base_url=args.server)

    try:
        summary = _sync(
            client, storage_path, args.direction, credentials_path=credentials_path
        )
        print(summary)
        if summary.errors:
            for error in summary.errors:
                print(f"Error: {error}", file=sys.stderr)
            return 1
        return 0
    except AuthenticationError as e:
        print(f"Authentication error: {e}", file=sys.stderr)
        print("Please log in with `snekdo login`.", file=sys.stderr)
        return 1
    except ConnectionError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ServerError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_register(args, parser) -> int:
    """Handle the register command by creating a new account on the server."""
    storage_path = _get_storage_path(args)
    credentials_path = _get_credentials_path(storage_path)
    client = ServerHttpClient(base_url=args.server)

    try:
        response = client._request(
            "POST",
            "/api/v1/auth/register",
            data={"username": args.username, "password": args.password},
            credentials_path=credentials_path,
        )
    except ServerError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ConnectionError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Store credentials
    token_type = response.get("token_type", "bearer")
    _write_credentials(credentials_path, response["access_token"], token_type)
    print(f"Registered user: {args.username}")
    print(f"Token stored to: {credentials_path}")
    return 0


def handle_login(args, parser) -> int:
    """Handle the login command by authenticating and storing the access token."""
    storage_path = _get_storage_path(args)
    credentials_path = _get_credentials_path(storage_path)
    client = ServerHttpClient(base_url=args.server)

    try:
        response = client._request(
            "POST",
            "/api/v1/auth/login",
            data={"username": args.username, "password": args.password},
            credentials_path=credentials_path,
        )
    except ServerError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ConnectionError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Store credentials
    token_type = response.get("token_type", "bearer")
    _write_credentials(credentials_path, response["access_token"], token_type)
    print(f"Logged in as: {args.username}")
    print(f"Token stored to: {credentials_path}")
    return 0


def handle_logout(args, parser) -> int:
    """Handle the logout command by removing stored credentials."""
    storage_path = _get_storage_path(args)
    credentials_path = _get_credentials_path(storage_path)
    _delete_credentials(credentials_path)
    print(f"Logged out. Credentials removed from: {credentials_path}")
    return 0


def handle_profile(args, parser) -> int:
    """Handle the profile command by fetching the current user's profile."""
    storage_path = _get_storage_path(args)
    credentials_path = _get_credentials_path(storage_path)
    client = ServerHttpClient(base_url=args.server)

    try:
        profile = client.get_profile(credentials_path=credentials_path)
    except AuthenticationError as e:
        print(f"Authentication error: {e}", file=sys.stderr)
        print("Please log in with `snekdo login`.", file=sys.stderr)
        return 1
    except ConnectionError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ServerError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(f"ID: {profile.get('id', '')}")
    print(f"Username: {profile.get('username', '')}")
    print(f"Display Name: {profile.get('display_name', '')}")
    print(f"Email: {profile.get('email', '')}")
    print(f"Created At: {profile.get('created_at', '')}")
    return 0


def handle_profile_update(args, parser) -> int:
    """Handle the profile-update command by updating the current user's profile."""
    storage_path = _get_storage_path(args)
    credentials_path = _get_credentials_path(storage_path)
    client = ServerHttpClient(base_url=args.server)

    try:
        response = client.update_profile(
            display_name=args.display_name,
            email=args.email,
            credentials_path=credentials_path,
        )
    except AuthenticationError as e:
        print(f"Authentication error: {e}", file=sys.stderr)
        print("Please log in with `snekdo login`.", file=sys.stderr)
        return 1
    except ConnectionError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ServerError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(f"Display Name: {response.get('display_name', '')}")
    print(f"Email: {response.get('email', '')}")
    print("Profile updated successfully.")
    return 0


def handle_change_password(args, parser) -> int:
    """Handle the change-password command by changing the current user's password."""
    storage_path = _get_storage_path(args)
    credentials_path = _get_credentials_path(storage_path)
    client = ServerHttpClient(base_url=args.server)

    try:
        response = client.change_password(
            current_password=args.current_password,
            new_password=args.new_password,
            confirm_password=args.confirm_password,
            credentials_path=credentials_path,
        )
    except AuthenticationError as e:
        print(f"Authentication error: {e}", file=sys.stderr)
        print("Please log in with `snekdo login`.", file=sys.stderr)
        return 1
    except ConnectionError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ServerError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(f"Message: {response.get('message', 'Password changed successfully.')}")
    return 0


def handle_delete_account(args, parser) -> int:
    """Handle the delete-account command by deleting the current user's account."""
    storage_path = _get_storage_path(args)
    credentials_path = _get_credentials_path(storage_path)
    client = ServerHttpClient(base_url=args.server)

    try:
        client.delete_account(
            password=args.password,
            credentials_path=credentials_path,
        )
    except AuthenticationError as e:
        print(f"Authentication error: {e}", file=sys.stderr)
        print("Please check your password.", file=sys.stderr)
        return 1
    except ConnectionError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ServerError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Remove stored credentials on success
    _delete_credentials(credentials_path)
    print("Account deleted successfully.")
    print(f"Credentials removed from: {credentials_path}")
    return 0


def _sync(
    client: ServerHttpClient,
    storage_path: Path,
    direction: str,
    credentials_path: Path | None = None,
) -> SyncSummary:
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
        server_todos = client.get_todos(credentials_path=credentials_path)
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
                        credentials_path=credentials_path,
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
                        completed=local_todo.completed,
                        credentials_path=credentials_path,
                    )
                    summary.updated += 1
                except (ConnectionError, ServerError) as e:
                    errors.append(f"Failed to update todo {local_todo.id}: {e}")

    # Delete server todos that no longer exist locally (only on push/both)
    if direction in ("push", "both"):
        for server_id in server_todo_map:
            if server_id not in local_todo_map:
                try:
                    client.delete_todo(server_id, credentials_path=credentials_path)
                    summary.deleted += 1
                except (ConnectionError, ServerError) as e:
                    errors.append(f"Failed to delete todo {server_id}: {e}")

    if errors:
        summary.errors = errors

    return summary


if __name__ == "__main__":
    sys.exit(main())
