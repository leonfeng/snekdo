"""Tests for the CLI layer."""

from unittest import mock
from pathlib import Path
import sys
from io import StringIO
from contextlib import contextmanager
from unittest.mock import patch

import pytest
import json

from nanoid import generate
from snekdo.models import Todo
from snekdo.storage import TodoStorage
from snekdo.__main__ import main, handle_command, handle_add, handle_list, handle_complete, handle_delete, handle_modify


class TestCLI:
    """Test cases for the CLI layer."""

    def test_add_todo(self, tmp_path):
        """Test adding a todo item."""
        # Create a temporary storage file
        storage_file = tmp_path / "todos.json"
        storage_file.write_text("[]")

        # Create mock args
        args = mock.MagicMock()
        args.command = "add"
        args.title = "Test todo"
        args.description = "A test todo"
        args.due = "2024-12-31"
        args.status = None
        args.limit = None
        args.todo_id = None
        args.storage = str(storage_file)

        # Mock the storage
        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = []
            
            # This would be called in handle_add
            from datetime import datetime
            todo = Todo(
                id=generate(),
                title=args.title,
                description=args.description,
                due=args.due,
                completed=False,
                created_at=datetime.now().isoformat(),
            )
            mock_storage_instance.load.return_value = []
            
            # Call the function
            result = handle_add(args, None)
            
            # Verify
            assert result == 0
            mock_storage_instance.add.assert_called_once()

    def test_list_todos(self, tmp_path):
        """Test listing todos."""
        # Create test data
        storage_file = tmp_path / "todos.json"
        todos = [
            {
                "id": "1",
                "title": "Test todo",
                "description": "A test todo",
                "due": "2024-12-31",
                "completed": False,
                "created_at": "2024-01-01T00:00:00",
            }
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "list"
        args.status = "all"
        args.limit = None
        args.todo_id = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = [
                Todo(
                    id="1",
                    title="Test todo",
                    description="A test todo",
                    due="2024-12-31",
                    completed=False,
                    created_at="2024-01-01T00:00:00",
                )
            ]
            
            result = handle_list(args, None)
            assert result == 0

    def test_complete_todo(self, tmp_path):
        """Test completing a todo."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {
                "id": "1",
                "title": "Test todo",
                "description": "",
                "due": None,
                "completed": False,
                "created_at": "2024-01-01T00:00:00",
            }
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "complete"
        args.todo_id = "1"
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            todo = Todo(
                id="1",
                title="Test todo",
                description="",
                due=None,
                completed=False,
                created_at="2024-01-01T00:00:00",
            )
            mock_storage_instance.get.return_value = todo
            
            result = handle_complete(args, None)
            assert result == 0

    def test_delete_todo(self, tmp_path):
        """Test deleting a todo."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {
                "id": "1",
                "title": "Test todo",
                "description": "",
                "due": None,
                "completed": False,
                "created_at": "2024-01-01T00:00:00",
            }
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "delete"
        args.todo_id = "1"
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            todo = Todo(
                id="1",
                title="Test todo",
                description="",
                due=None,
                completed=False,
                created_at="2024-01-01T00:00:00",
            )
            mock_storage_instance.get.return_value = todo
            
            result = handle_delete(args, None)
            assert result == 0

    def test_main_entry_point(self):
        """Test the main entry point."""
        with patch('snekdo.__main__.argparse') as mock_argparse:
            parser = mock_argparse.ArgumentParser()
            args = mock_argparse.Namespace()
            args.command = None
            args.storage = None
            args.debug = False
            mock_argparse.Namespace.return_value = args
            mock_argparse.ArgumentParser.return_value.parse_args.return_value = args
            
            result = main()
            assert result == 0

    def test_modify_todo(self, tmp_path):
        """Test modifying a todo."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {
                "id": "1",
                "title": "Test todo",
                "description": "A test todo",
                "due": "2024-12-31",
                "completed": False,
                "created_at": "2024-01-01T00:00:00",
            }
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "modify"
        args.todo_id = "1"
        args.title = "Updated title"
        args.description = None
        args.due = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            todo = Todo(
                id="1",
                title="Test todo",
                description="A test todo",
                due="2024-12-31",
                completed=False,
                created_at="2024-01-01T00:00:00",
            )
            mock_storage_instance.get.return_value = todo
            
            result = handle_modify(args, None)
            assert result == 0
            mock_storage_instance.modify.assert_called_once()

    def test_modify_not_found(self, tmp_path):
        """Test modifying a non-existent todo."""
        storage_file = tmp_path / "todos.json"
        storage_file.write_text("[]")

        args = mock.MagicMock()
        args.command = "modify"
        args.todo_id = "nonexistent"
        args.title = "Updated title"
        args.description = None
        args.due = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.get.return_value = None
            
            result = handle_modify(args, None)
            assert result == 1

    def test_modify_no_fields(self, tmp_path):
        """Test modifying with no fields to update."""
        storage_file = tmp_path / "todos.json"
        storage_file.write_text("[]")

        args = mock.MagicMock()
        args.command = "modify"
        args.todo_id = "1"
        args.title = None
        args.description = None
        args.due = None
        args.storage = str(storage_file)

        result = handle_modify(args, None)
        assert result == 1

    def test_modify_empty_string_title(self, tmp_path):
        """Test modifying with an empty string title."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {
                "id": "1",
                "title": "Test todo",
                "description": "A test todo",
                "due": "2024-12-31",
                "completed": False,
                "created_at": "2024-01-01T00:00:00",
            }
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "modify"
        args.todo_id = "1"
        args.title = ""
        args.description = None
        args.due = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            todo = Todo(
                id="1",
                title="Test todo",
                description="A test todo",
                due="2024-12-31",
                completed=False,
                created_at="2024-01-01T00:00:00",
            )
            mock_storage_instance.get.return_value = todo
            result = handle_modify(args, None)
            assert result == 0

    def test_modify_clear_description(self, tmp_path):
        """Test clearing the description."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {
                "id": "1",
                "title": "Test todo",
                "description": "A test todo",
                "due": "2024-12-31",
                "completed": False,
                "created_at": "2024-01-01T00:00:00",
            }
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "modify"
        args.todo_id = "1"
        args.title = None
        args.description = ""
        args.due = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            todo = Todo(
                id="1",
                title="Test todo",
                description="A test todo",
                due="2024-12-31",
                completed=False,
                created_at="2024-01-01T00:00:00",
            )
            mock_storage_instance.get.return_value = todo
            result = handle_modify(args, None)
            assert result == 0

    def test_modify_clear_due(self, tmp_path):
        """Test clearing the due date."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {
                "id": "1",
                "title": "Test todo",
                "description": "A test todo",
                "due": "2024-12-31",
                "completed": False,
                "created_at": "2024-01-01T00:00:00",
            }
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "modify"
        args.todo_id = "1"
        args.title = None
        args.description = None
        args.due = ""
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            todo = Todo(
                id="1",
                title="Test todo",
                description="A test todo",
                due="2024-12-31",
                completed=False,
                created_at="2024-01-01T00:00:00",
            )
            mock_storage_instance.get.return_value = todo
            result = handle_modify(args, None)
            assert result == 0

    def test_modify_partial_update(self, tmp_path):
        """Test that modifying one field doesn't affect others."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {
                "id": "1",
                "title": "Test todo",
                "description": "A test todo",
                "due": "2024-12-31",
                "completed": False,
                "created_at": "2024-01-01T00:00:00",
            }
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "modify"
        args.todo_id = "1"
        args.title = "Updated Title"
        args.description = None
        args.due = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            todo = Todo(
                id="1",
                title="Test todo",
                description="A test todo",
                due="2024-12-31",
                completed=False,
                created_at="2024-01-01T00:00:00",
            )
            mock_storage_instance.get.return_value = todo
            result = handle_modify(args, None)
            assert result == 0
            mock_storage_instance.modify.assert_called_once_with("1", title="Updated Title")

    def test_add_todo_with_priority(self, tmp_path):
        """Test adding a todo with priority."""
        storage_file = tmp_path / "todos.json"
        storage_file.write_text("[]")

        args = mock.MagicMock()
        args.command = "add"
        args.title = "Test todo"
        args.description = "A test todo"
        args.due = "2024-12-31"
        args.priority = "high"
        args.status = None
        args.limit = None
        args.todo_id = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            result = handle_add(args, None)
            assert result == 0
            mock_storage_instance.add.assert_called_once()
            called_todo = mock_storage_instance.add.call_args[0][0]
            assert called_todo.priority == "high"

    def test_list_with_priority_filter(self, tmp_path):
        """Test listing todos with priority filter."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {
                "id": "1",
                "title": "High Priority",
                "description": "",
                "due": None,
                "completed": False,
                "created_at": "2024-01-01T00:00:00",
                "priority": "high",
            },
            {
                "id": "2",
                "title": "Low Priority",
                "description": "",
                "due": None,
                "completed": False,
                "created_at": "2024-01-02T00:00:00",
                "priority": "low",
            }
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "list"
        args.status = "all"
        args.limit = None
        args.todo_id = None
        args.priority = "high"
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = [
                Todo(
                    id="1",
                    title="High Priority",
                    description="",
                    due=None,
                    completed=False,
                    created_at="2024-01-01T00:00:00",
                    priority="high",
                ),
                Todo(
                    id="2",
                    title="Low Priority",
                    description="",
                    due=None,
                    completed=False,
                    created_at="2024-01-02T00:00:00",
                    priority="low",
                )
            ]
            result = handle_list(args, None)
            assert result == 0
            assert len(mock_storage_instance.load.return_value) == 1
            assert mock_storage_instance.load.return_value[0].priority == "high"

    def test_modify_todo_with_priority(self, tmp_path):
        """Test modifying a todo's priority."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {
                "id": "1",
                "title": "Test todo",
                "description": "A test todo",
                "due": "2024-12-31",
                "completed": False,
                "created_at": "2024-01-01T00:00:00",
                "priority": "low",
            }
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "modify"
        args.todo_id = "1"
        args.title = None
        args.description = None
        args.due = None
        args.priority = "high"
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            todo = Todo(
                id="1",
                title="Test todo",
                description="A test todo",
                due="2024-12-31",
                completed=False,
                created_at="2024-01-01T00:00:00",
                priority="low",
            )
            mock_storage_instance.get.return_value = todo
            result = handle_modify(args, None)
            assert result == 0
            mock_storage_instance.modify.assert_called_once()
            call_args = mock_storage_instance.modify.call_args
            assert call_args[1]["priority"] == "high"
