"""CLI entry point for the snekdo application."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from snekdo.models import Todo
from snekdo.storage import StorageError, TodoStorage


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="snekdo",
        description="A simple CLI todo list manager",
    )
    parser.add_argument("--storage", help="Path to the storage file")
    parser.add_argument("--debug", action="store_true", help="Print debug information")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new todo item")
    add_parser.add_argument("--title", required=True, help="Title of the todo")
    add_parser.add_argument("--description", default="", help="Description of the todo")
    add_parser.add_argument("--due", help="Due date (e.g., 2024-12-31)")
    add_parser.add_argument("--priority", default="medium", choices=["low", "medium", "high"], help="Priority level (low, medium, high)")

    # List command
    list_parser = subparsers.add_parser("list", help="List all todo items")
    list_parser.add_argument("--status", choices=["all", "pending", "completed"], default="all")
    list_parser.add_argument("--limit", type=int, help="Limit the number of results")
    list_parser.add_argument("--priority", default=None, choices=["low", "medium", "high"], help="Filter by priority level")
    list_parser.add_argument("--sort", default="created_at", choices=["created_at", "title", "priority", "completed"], help="Sort by field (created_at, title, priority, completed)")
    list_parser.add_argument("--reverse", action="store_true", default=False, dest="reverse", help="Reverse the sort order")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a todo as complete")
    complete_parser.add_argument("todo_id", help="ID of the todo to complete")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a todo")
    delete_parser.add_argument("todo_id", help="ID of the todo to delete")

    # Modify command
    modify_parser = subparsers.add_parser("modify", help="Modify an existing todo")
    modify_parser.add_argument("todo_id", help="ID of the todo to modify")
    modify_parser.add_argument("--title", help="New title for the todo")
    modify_parser.add_argument("--description", default=None, help="New description for the todo")
    modify_parser.add_argument("--due", help="New due date for the todo (e.g., 2024-12-31)")
    modify_parser.add_argument("--priority", default=None, choices=["low", "medium", "high"], help="New priority level")

    try:
        args = parser.parse_args()
        return handle_command(args, parser)
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 1


def handle_command(args, parser) -> int:
    """Handle the parsed command line arguments."""
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
    storage = TodoStorage(storage_path=args.storage)
    todo = Todo(
        title=args.title,
        description=args.description,
        due=args.due,
        completed=False,
        created_at=datetime.now().isoformat(),
        priority=args.priority,
    )
    storage.add(todo)
    print(f"Added todo: {todo.title}")
    return 0


def handle_list(args, parser) -> int:
    """Handle the list command."""
    storage = TodoStorage(storage_path=args.storage)
    todos = storage.load()

    # Filter by status
    if args.status == "pending":
        todos = [t for t in todos if not t.completed]
    elif args.status == "completed":
        todos = [t for t in todos if t.completed]

    # Filter by priority
    if args.priority:
        todos = [t for t in todos if t.priority == args.priority]

    # Sort by the specified field
    sort_key = args.sort
    if sort_key == "created_at":
        todos = sorted(todos, key=lambda x: x.created_at, reverse=args.reverse)
    elif sort_key == "title":
        todos = sorted(todos, key=lambda x: x.title.lower(), reverse=args.reverse)
    elif sort_key == "priority":
        priority_order = {"high": 0, "medium": 1, "low": 2}
        todos = sorted(todos, key=lambda x: priority_order.get(x.priority, 1), reverse=args.reverse)
    elif sort_key == "completed":
        todos = sorted(todos, key=lambda x: x.completed, reverse=args.reverse)
    else:
        # Default to created_at if unknown sort field
        todos = sorted(todos, key=lambda x: x.created_at, reverse=args.reverse)

    # Limit results
    if args.limit:
        todos = todos[:args.limit]

    if not todos:
        print("No todos found.")
        return 0

    print(f"{'ID':<35} {'Title':<30} {'Status':<10} {'Priority':<10} {'Due':<15}")
    print("-" * 100)
    for todo in todos:
        status = "✓" if todo.completed else " "
        due = todo.due if todo.due else ""
        print(f"{todo.id:<35} {todo.title:<30} {status:<10} {todo.priority:<10} {due:<15}")

    return 0


def handle_complete(args, parser) -> int:
    """Handle the complete command."""
    storage = TodoStorage(storage_path=args.storage)
    todo = storage.get(args.todo_id)
    if todo is None:
        print(f"Error: Todo with ID {args.todo_id} not found")
        return 1
    storage.complete(args.todo_id)
    print(f"Completed todo: {todo.title}")
    return 0


def handle_delete(args, parser) -> int:
    """Handle the delete command."""
    storage = TodoStorage(storage_path=args.storage)
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

    storage = TodoStorage(storage_path=args.storage)
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
        update_data["due"] = args.due
    if args.priority is not None:
        update_data["priority"] = args.priority

    storage.modify(args.todo_id, **update_data)
    print(f"Updated todo: {todo.title}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
