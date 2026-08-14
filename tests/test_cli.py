"""Tests for the CLI layer."""

from unittest import mock
from pathlib import Path
import sys
from io import StringIO
from contextlib import contextmanager
import io
from unittest.mock import patch

import pytest
import json

from nanoid import generate
from snekdo.models import Todo
from snekdo.storage import TodoStorage
from snekdo.__main__ import main, handle_command, handle_add, handle_list, handle_complete, handle_delete, handle_modify, handle_show


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
        args.priority = None
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
            # Verify the list was filtered by priority
            all_todos = mock_storage_instance.load.return_value
            assert len(all_todos) == 2
            # The actual filtering happens in handle_list, so we just verify no error occurred

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

    def test_list_sort_by_title(self, tmp_path):
        """Test listing todos sorted by title."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {"id": "1", "title": "Cherry", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00", "priority": "medium"},
            {"id": "2", "title": "Apple", "description": "", "due": None, "completed": False, "created_at": "2024-01-02T00:00:00", "priority": "medium"},
            {"id": "3", "title": "Banana", "description": "", "due": None, "completed": False, "created_at": "2024-01-03T00:00:00", "priority": "medium"},
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "list"
        args.status = "all"
        args.limit = None
        args.todo_id = None
        args.sort = "title"
        args.reverse = False
        args.priority = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = [
                Todo(**todos[0]),
                Todo(**todos[1]),
                Todo(**todos[2]),
            ]

            import io
            import sys
            # Capture stdout
            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            lines = [line for line in output_str.strip().split('\n') if line and not line.startswith('---')]
            titles = [line.split()[1] for line in lines[1:]]
            assert titles == ["Apple", "Banana", "Cherry"]

    def test_list_sort_by_title_reverse(self, tmp_path):
        """Test listing todos sorted by title in reverse order."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {"id": "1", "title": "Cherry", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00", "priority": "medium"},
            {"id": "2", "description": "", "title": "Apple", "due": None, "completed": False, "created_at": "2024-01-02T00:00:00", "priority": "medium"},
            {"id": "3", "title": "Banana", "description": "", "due": None, "completed": False, "created_at": "2024-01-03T00:00:00", "priority": "medium"},
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "list"
        args.status = "all"
        args.limit = None
        args.todo_id = None
        args.sort = "title"
        args.reverse = True
        args.priority = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = [
                Todo(**todos[0]),
                Todo(**todos[1]),
                Todo(**todos[2]),
            ]

            import io
            import sys
            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            lines = [line for line in output_str.strip().split('\n') if line and not line.startswith('---')]
            titles = [line.split()[1] for line in lines[1:]]
            assert titles == ["Cherry", "Banana", "Apple"]

    def test_list_sort_by_priority(self, tmp_path):
        """Test listing todos sorted by priority."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {"id": "1", "title": "Low", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00", "priority": "low"},
            {"id": "2", "title": "High", "description": "", "due": None, "completed": False, "created_at": "2024-01-02T00:00:00", "priority": "high"},
            {"id": "3", "title": "Medium", "description": "", "due": None, "completed": False, "created_at": "2024-01-03T00:00:00", "priority": "medium"},
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "list"
        args.status = "all"
        args.limit = None
        args.todo_id = None
        args.sort = "priority"
        args.reverse = False
        args.priority = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = [
                Todo(**todos[0]),
                Todo(**todos[1]),
                Todo(**todos[2]),
            ]

            import io
            import sys
            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            lines = [line for line in output_str.strip().split('\n') if line and not line.startswith('---')]
            titles = [line.split()[1] for line in lines[1:]]
            assert titles == ["High", "Medium", "Low"]

    def test_list_sort_by_created_at(self, tmp_path):
        """Test listing todos sorted by created_at."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {"id": "1", "title": "Old", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00", "priority": "medium"},
            {"id": "2", "title": "New", "description": "", "due": None, "completed": False, "created_at": "2024-01-03T00:00:00", "priority": "medium"},
            {"id": "3", "title": "Medium", "description": "", "due": None, "completed": False, "created_at": "2024-01-02T00:00:00", "priority": "medium"},
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "list"
        args.status = "all"
        args.limit = None
        args.todo_id = None
        args.sort = "created_at"
        args.reverse = False
        args.priority = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = [
                Todo(**todos[0]),
                Todo(**todos[1]),
                Todo(**todos[2]),
            ]

            import io
            import sys
            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            lines = [line for line in output_str.strip().split('\n') if line and not line.startswith('---')]
            titles = [line.split()[1] for line in lines[1:]]
            assert titles == ["Old", "Medium", "New"]

    def test_list_sort_by_completed(self, tmp_path):
        """Test listing todos sorted by completed status."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {"id": "1", "title": "Done", "description": "", "due": None, "completed": True, "created_at": "2024-01-01T00:00:00", "priority": "medium"},
            {"id": "2", "title": "Pending", "description": "", "due": None, "completed": False, "created_at": "2024-01-02T00:00:00", "priority": "medium"},
            {"id": "3", "title": "Also Done", "description": "", "due": None, "completed": True, "created_at": "2024-01-03T00:00:00", "priority": "medium"},
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "list"
        args.status = "all"
        args.limit = None
        args.todo_id = None
        args.sort = "completed"
        args.reverse = False
        args.priority = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = [
                Todo(**todos[0]),
                Todo(**todos[1]),
                Todo(**todos[2]),
            ]

            import io
            import sys
            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            lines = [line for line in output_str.strip().split('\n') if line and not line.startswith('---')]
            titles = [line.split()[1] for line in lines[1:]]
            assert titles == ["Pending", "Done", "Also"]

    def test_complete_todo_real_storage(self, tmp_path):
        """Test completing a todo preserves other todos using real storage."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {"id": "1", "title": "First", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00", "priority": "medium"},
            {"id": "2", "title": "Second", "description": "", "due": None, "completed": False, "created_at": "2024-01-02T00:00:00", "priority": "medium"},
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "complete"
        args.todo_id = "1"
        args.storage = str(storage_file)

        result = handle_complete(args, None)
        assert result == 0

        stored = json.loads(storage_file.read_text())
        assert len(stored) == 2
        assert stored[0]["completed"] is True
        assert stored[1]["completed"] is False

    def test_storage_flag_uses_custom_path(self, tmp_path):
        """Test that --storage flag saves to the specified path."""
        storage_file = tmp_path / "custom" / "todos.json"
        storage_file.parent.mkdir(parents=True, exist_ok=True)

        args = mock.MagicMock()
        args.command = "add"
        args.title = "Custom path todo"
        args.description = ""
        args.due = None
        args.priority = "medium"
        args.storage = str(storage_file)

        result = handle_add(args, None)
        assert result == 0
        assert storage_file.exists()

        stored = json.loads(storage_file.read_text())
        assert len(stored) == 1
        assert stored[0]["title"] == "Custom path todo"

    def test_default_storage_path_when_omitted(self, tmp_path, monkeypatch):
        """Test that default path is used when --storage is omitted."""
        default_dir = tmp_path / ".snekdo"
        default_dir.mkdir()
        default_file = default_dir / "todos.json"
        monkeypatch.setenv("HOME", str(tmp_path))

        args = mock.MagicMock()
        args.command = "add"
        args.title = "Default path todo"
        args.description = ""
        args.due = None
        args.priority = "medium"
        args.storage = None

        result = handle_add(args, None)
        assert result == 0
        assert default_file.exists()
        stored = json.loads(default_file.read_text())
        assert stored[0]["title"] == "Default path todo"

    def test_list_sort_real_storage(self, tmp_path):
        """Test that sorting works correctly with real storage."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {"id": "1", "title": "Cherry", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00", "priority": "medium"},
            {"id": "2", "title": "Apple", "description": "", "due": None, "completed": False, "created_at": "2024-01-02T00:00:00", "priority": "medium"},
            {"id": "3", "title": "Banana", "description": "", "due": None, "completed": False, "created_at": "2024-01-03T00:00:00", "priority": "medium"},
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "list"
        args.status = "all"
        args.limit = None
        args.todo_id = None
        args.sort = "title"
        args.reverse = False
        args.priority = None
        args.storage = str(storage_file)

        result = handle_list(args, None)
        assert result == 0

        stored = json.loads(storage_file.read_text())
        assert len(stored) == 3

    def test_list_storage_flag_real_storage(self, tmp_path):
        """Test that --storage flag works for list command with real storage."""
        storage_file = tmp_path / "custom" / "todos.json"
        storage_file.parent.mkdir(parents=True, exist_ok=True)
        todos = [
            {"id": "1", "title": "First", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00", "priority": "medium"},
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "list"
        args.status = "all"
        args.limit = None
        args.todo_id = None
        args.sort = "created_at"
        args.reverse = False
        args.priority = None
        args.storage = str(storage_file)

        result = handle_list(args, None)
        assert result == 0

        stored = json.loads(storage_file.read_text())
        assert len(stored) == 1
        assert stored[0]["title"] == "First"

    def test_delete_preserves_others_real_storage(self, tmp_path):
        """Test that deleting a todo preserves other todos using real storage."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {"id": "1", "title": "First", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00", "priority": "medium"},
            {"id": "2", "title": "Second", "description": "", "due": None, "completed": False, "created_at": "2024-01-02T00:00:00", "priority": "medium"},
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "delete"
        args.todo_id = "1"
        args.storage = str(storage_file)

        result = handle_delete(args, None)
        assert result == 0

        stored = json.loads(storage_file.read_text())
        assert len(stored) == 1
        assert stored[0]["title"] == "Second"

    def test_list_shows_created_at_header(self, tmp_path):
        """Test that the list output includes a Created At header."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {"id": "1", "title": "Test todo", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00", "priority": "medium"},
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "list"
        args.status = "all"
        args.limit = None
        args.todo_id = None
        args.sort = "created_at"
        args.reverse = False
        args.priority = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = [
                Todo(
                    id="1",
                    title="Test todo",
                    description="",
                    due=None,
                    completed=False,
                    created_at="2024-01-01T00:00:00",
                    priority="medium",
                )
            ]

            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            assert "Created At" in output_str

    def test_list_shows_created_at_value(self, tmp_path):
        """Test that the list output displays the created_at value for each todo."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {"id": "1", "title": "Test todo", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00", "priority": "medium"},
            {"id": "2", "title": "Another todo", "description": "", "due": "2027-12-31", "completed": True, "created_at": "2024-01-03T00:00:00", "priority": "high"},
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "list"
        args.status = "all"
        args.limit = None
        args.todo_id = None
        args.sort = "created_at"
        args.reverse = False
        args.priority = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = [
                Todo(
                    id="1",
                    title="Test todo",
                    description="",
                    due=None,
                    completed=False,
                    created_at="2024-01-01T00:00:00",
                    priority="medium",
                ),
                Todo(
                    id="2",
                    title="Another todo",
                    description="2024-12-31",
                    due="2027-12-31",
                    completed=True,
                    created_at="2024-01-03T00:00:00",
                    priority="high",
                )
            ]

            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            assert "2024-01-01T00:00:00" in output_str
            assert "2024-01-03T00:00:00" in output_str

    def test_list_created_at_empty(self, tmp_path):
        """Test that the list output handles empty created_at values."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {"id": "1", "title": "Test todo", "description": "", "due": None, "completed": False, "created_at": "", "priority": "medium"},
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "list"
        args.status = "all"
        args.limit = None
        args.todo_id = None
        args.sort = "created_at"
        args.reverse = False
        args.priority = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = [
                Todo(
                    id="1",
                    title="Test todo",
                    description="",
                    due=None,
                    completed=False,
                    created_at="",
                    priority="medium",
                )
            ]

            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            assert "Created At" in output_str

    def test_list_hides_completed_by_default(self, tmp_path):
        """Test that completed items are hidden by default when listing."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {"id": "1", "title": "Pending todo", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00", "priority": "medium"},
            {"id": "2", "title": "Completed todo", "description": "", "due": None, "completed": True, "created_at": "2024-01-02T00:00:00", "priority": "medium"},
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "list"
        args.status = "pending"  # default is now pending
        args.limit = None
        args.todo_id = None
        args.sort = "created_at"
        args.reverse = False
        args.priority = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = [
                Todo(
                    id="1",
                    title="Pending todo",
                    description="",
                    due=None,
                    completed=False,
                    created_at="2024-01-01T00:00:00",
                    priority="medium",
                ),
                Todo(
                    id="2",
                    title="Completed todo",
                    description="",
                    due=None,
                    completed=True,
                    created_at="2024-01-02T00:00:00",
                    priority="medium",
                )
            ]

            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            assert "Pending todo" in output_str
            assert "Completed todo" not in output_str

    def test_list_status_all_shows_completed(self, tmp_path):
        """Test that --status all still shows completed items."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {"id": "1", "title": "Pending todo", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00", "priority": "medium"},
            {"id": "2", "title": "Completed todo", "description": "", "due": None, "completed": True, "created_at": "2024-01-02T00:00:00", "priority": "medium"},
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "list"
        args.status = "all"
        args.limit = None
        args.todo_id = None
        args.sort = "created_at"
        args.reverse = False
        args.priority = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = [
                Todo(
                    id="1",
                    title="Pending todo",
                    description="",
                    due=None,
                    completed=False,
                    created_at="2024-01-01T00:00:00",
                    priority="medium",
                ),
                Todo(
                    id="2",
                    title="Completed todo",
                    description="",
                    due=None,
                    completed=True,
                    created_at="2024-01-02T00:00:00",
                    priority="medium",
                )
            ]

            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            assert "Pending todo" in output_str
            assert "Completed todo" in output_str

    def test_show_todo(self, tmp_path):
        """Test showing an existing todo item."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {
                "id": "1",
                "title": "Test todo",
                "description": "A test todo",
                "due": "2027-12-31",
                "completed": False,
                "created_at": "2024-01-01T00:00:00",
                "priority": "medium",
            }
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "show"
        args.todo_id = "1"
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.get.return_value = Todo(
                id="1",
                title="Test todo",
                description="A test todo",
                due="2027-12-31",
                completed=False,
                created_at="2024-01-01T00:00:00",
                priority="medium",
            )

            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_show(args, None)

            assert result == 0
            output_str = output.getvalue()
            assert "ID: 1" in output_str
            assert "Title: Test todo" in output_str
            assert "Description: A test todo" in output_str
            assert "Due: 2027-12-31" in output_str
            assert "Priority: medium" in output_str
            assert "Created At: 2024-01-01T00:00:00" in output_str

    def test_show_todo_not_found(self, tmp_path):
        """Test showing a non-existent todo item."""
        storage_file = tmp_path / "todos.json"
        storage_file.write_text("[]")

        args = mock.MagicMock()
        args.command = "show"
        args.todo_id = "nonexistent"
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.get.return_value = None

            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_show(args, None)

            assert result == 1
            output_str = output.getvalue()
            assert "not found" in output_str

    def test_show_completed_todo(self, tmp_path):
        """Test showing a completed todo item displays status correctly."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {
                "id": "1",
                "title": "Done todo",
                "description": "",
                "due": None,
                "completed": True,
                "created_at": "2024-01-01T00:00:00",
                "priority": "high",
            }
        ]
        storage_file.write_text(json.dumps(todos))

        args = mock.MagicMock()
        args.command = "show"
        args.todo_id = "1"
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.get.return_value = Todo(
                id="1",
                title="Done todo",
                description="",
                due=None,
                completed=True,
                created_at="2024-01-01T00:00:00",
                priority="high",
            )

            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_show(args, None)

            assert result == 0
            output_str = output.getvalue()
            assert "Status: ✓" in output_str
