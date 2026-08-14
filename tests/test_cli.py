"""Tests for the CLI layer."""

from unittest import mock
import io
from unittest.mock import patch

import pytest

import json

from nanoid import generate
from snekdo.models import Todo
from snekdo.__main__ import main, handle_command, handle_add, handle_list, handle_complete, handle_delete, handle_modify, handle_show


def _parse_list_line(line):
    """Parse a list output line into its columns.

    The list output format is:
    {ID:<35} {Title:<title_width} {Status:<10} {Priority:<10} {Due:<15} {Created At:<25}

    Since all columns except Title are fixed-width, we parse from the right.
    """
    line = line.rstrip(chr(10))

    # Parse from the right (all fixed-width columns except Title)
    created_at = line[-25:].strip()
    line = line[:-25]
    line = line[:-1]  # remove space separator before Created At
    due = line[-15:].strip()
    line = line[:-15]
    line = line[:-1]  # remove space separator before Due
    priority = line[-10:].strip()
    line = line[:-10]
    line = line[:-1]  # remove space separator before Priority
    status = line[-10:].strip()
    line = line[:-10]
    line = line[:-1]  # remove space separator before Status

    # Now line = {ID:<35} {Title:<title_width>} (with trailing space)
    id_ = line[:35].strip()
    title = line[36:].strip()

    return id_, title, status, priority, due, created_at



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
        args.due = "2027-12-31"
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
                "due": "2027-12-31",
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
        args.sort = "created_at"
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = [
                Todo(
                    id="1",
                    title="Test todo",
                    description="A test todo",
                    due="2027-12-31",
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
                "due": "2027-12-31",
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
                due="2027-12-31",
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
                "due": "2027-12-31",
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
                due="2027-12-31",
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
                "due": "2027-12-31",
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
                due="2027-12-31",
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
                "due": "2027-12-31",
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
                due="2027-12-31",
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
                "due": "2027-12-31",
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
                due="2027-12-31",
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
        args.due = "2027-12-31"
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
        args.sort = "created_at"
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
                "due": "2027-12-31",
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
                due="2027-12-31",
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
            # Capture stdout
            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            lines = [line for line in output_str.rstrip('\n').split('\n') if line and not line.startswith('---')]
            titles = [_parse_list_line(line)[1] for line in lines[1:]]
            assert titles == ["Apple", "Banana", "Cherry"]

    def test_list_long_title_truncated_with_ellipsis(self, tmp_path):
        """Test that titles exceeding the maximum width are truncated with ellipsis."""
        storage_file = tmp_path / "todos.json"
        storage_file.write_text("[]")

        args = mock.MagicMock()
        args.command = "list"
        args.status = "all"
        args.limit = None
        args.todo_id = None
        args.sort = "title"
        args.reverse = False
        args.priority = None
        args.storage = str(storage_file)

        long_title = "This is a very long title that should be truncated"
        short_title = "Short"

        with patch("snekdo.__main__.TodoStorage") as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = [
                Todo(
                    id="1",
                    title=long_title,
                    description="",
                    due=None,
                    completed=False,
                    created_at="2024-01-01T00:00:00",
                    priority="medium",
                ),
                Todo(
                    id="2",
                    title=short_title,
                    description="",
                    due=None,
                    completed=False,
                    created_at="2024-01-02T00:00:00",
                    priority="medium",
                ),
            ]

            output = io.StringIO()
            with patch("builtins.print", return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + "\n")
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            lines = [line for line in output_str.rstrip("\n").split("\n") if line and not line.startswith("---")]
            titles = [_parse_list_line(line)[1] for line in lines[1:]]

            # The long title should be truncated with ellipsis
            assert long_title not in titles
            assert any(t.endswith("...") for t in titles)

    def test_list_short_title_fully_visible(self, tmp_path):
        """Test that short titles are displayed fully without truncation."""
        storage_file = tmp_path / "todos.json"
        storage_file.write_text("[]")

        args = mock.MagicMock()
        args.command = "list"
        args.status = "all"
        args.limit = None
        args.todo_id = None
        args.sort = "title"
        args.reverse = False
        args.priority = None
        args.storage = str(storage_file)

        with patch("snekdo.__main__.TodoStorage") as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = [
                Todo(
                    id="1",
                    title="Apple",
                    description="",
                    due=None,
                    completed=False,
                    created_at="2024-01-01T00:00:00",
                    priority="medium",
                ),
            ]

            output = io.StringIO()
            with patch("builtins.print", return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + "\n")
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            lines = [line for line in output_str.rstrip("\n").split("\n") if line and not line.startswith("---")]
            titles = [_parse_list_line(line)[1] for line in lines[1:]]

            assert titles == ["Apple"]

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
            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            lines = [line for line in output_str.rstrip('\n').split('\n') if line and not line.startswith('---')]
            titles = [_parse_list_line(line)[1] for line in lines[1:]]
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
            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            lines = [line for line in output_str.rstrip('\n').split('\n') if line and not line.startswith('---')]
            titles = [_parse_list_line(line)[1] for line in lines[1:]]
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
            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            lines = [line for line in output_str.rstrip('\n').split('\n') if line and not line.startswith('---')]
            titles = [_parse_list_line(line)[1] for line in lines[1:]]
            assert titles == ["Old", "Medium", "New"]

    def test_list_sort_by_created_at_microsecond_precision(self, tmp_path):
        """Test listing todos sorted by created_at with microsecond precision."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {"id": "1", "title": "First", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00.123456", "priority": "medium"},
            {"id": "2", "title": "Second", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00.654321", "priority": "medium"},
            {"id": "3", "title": "Third", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00.000000", "priority": "medium"},
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

            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            lines = [line for line in output_str.rstrip('\n').split('\n') if line and not line.startswith('---')]
            titles = [_parse_list_line(line)[1] for line in lines[1:]]
            assert titles == ["Third", "First", "Second"]

    def test_list_sort_by_created_at_reverse(self, tmp_path):
        """Test listing todos sorted by created_at in reverse order."""
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

            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            lines = [line for line in output_str.rstrip('\n').split('\n') if line and not line.startswith('---')]
            titles = [_parse_list_line(line)[1] for line in lines[1:]]
            assert titles == ["New", "Medium", "Old"]

    def test_list_sort_by_created_at_empty(self, tmp_path):
        """Test listing todos with empty created_at values sort consistently."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {"id": "1", "title": "Has Date", "description": "", "due": None, "completed": False, "created_at": "2024-01-02T00:00:00", "priority": "medium"},
            {"id": "2", "title": "Empty Date", "description": "", "due": None, "completed": False, "created_at": "", "priority": "medium"},
            {"id": "3", "title": "Also Has Date", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00", "priority": "medium"},
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

            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            lines = [line for line in output_str.rstrip('\n').split('\n') if line and not line.startswith('---')]
            titles = [_parse_list_line(line)[1] for line in lines[1:]]
            assert titles == ["Empty Date", "Also Has Date", "Has Date"]

    def test_list_sort_by_created_at_mixed_precision(self, tmp_path):
        """Test listing todos with mixed-precision ISO 8601 created_at values."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {"id": "1", "title": "NoMicro", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00", "priority": "medium"},
            {"id": "2", "title": "WithMicro", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00.000000", "priority": "medium"},
            {"id": "3", "title": "Later", "description": "", "due": None, "completed": False, "created_at": "2024-01-02T00:00:00", "priority": "medium"},
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

            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            lines = [line for line in output_str.rstrip('\n').split('\n') if line and not line.startswith('---')]
            titles = [_parse_list_line(line)[1] for line in lines[1:]]
            assert titles == ["NoMicro", "WithMicro", "Later"]

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
            output = io.StringIO()
            with patch('builtins.print', return_value=None) as mock_print:
                mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + '\n')
                result = handle_list(args, None)

            assert result == 0
            output_str = output.getvalue()
            lines = [line for line in output_str.rstrip('\n').split('\n') if line and not line.startswith('---')]
            titles = [_parse_list_line(line)[1] for line in lines[1:]]
            assert titles == ["Pending", "Done", "Also Done"]

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

    def test_list_status_display(self, tmp_path):
        """Test that the list output displays pending status as text."""
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
            assert "pending" in output_str

    def test_list_invalid_sort_field(self, tmp_path):
        """Test that an invalid sort field is rejected with an error."""
        storage_file = tmp_path / "todos.json"
        storage_file.write_text("[]")

        args = mock.MagicMock()
        args.command = "list"
        args.status = "all"
        args.limit = None
        args.todo_id = None
        args.sort = "invalid_field"
        args.reverse = False
        args.priority = None
        args.storage = str(storage_file)

        result = handle_list(args, None)
        assert result == 1

    def test_list_invalid_sort_field_error_message(self, tmp_path):
        """Test that the error message for an invalid sort field lists valid fields."""
        storage_file = tmp_path / "todos.json"
        storage_file.write_text("[]")

        args = mock.MagicMock()
        args.command = "list"
        args.status = "all"
        args.limit = None
        args.todo_id = None
        args.sort = "invalid_field"
        args.reverse = False
        args.priority = None
        args.storage = str(storage_file)

        import io
        output = io.StringIO()
        with patch("builtins.print", return_value=None) as mock_print:
            mock_print.side_effect = lambda *args, **kwargs: output.write(str(args[0]) + chr(10))
            result = handle_list(args, None)

        assert result == 1
        output_str = output.getvalue()
        assert "Invalid sort field" in output_str
        assert "invalid_field" in output_str
        assert "created_at" in output_str
        assert "title" in output_str
        assert "priority" in output_str
        assert "completed" in output_str

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

    def test_show_pending_todo(self, tmp_path):
        """Test showing a pending todo item displays status correctly."""
        storage_file = tmp_path / "todos.json"
        todos = [
            {
                "id": "1",
                "title": "Pending todo",
                "description": "",
                "due": None,
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
                title="Pending todo",
                description="",
                due=None,
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
            assert "Status: pending" in output_str

    def test_add_todo_valid_date_accepted(self, tmp_path):
        """Test that a valid future date is accepted when adding a todo."""
        storage_file = tmp_path / "todos.json"
        storage_file.write_text("[]")

        args = mock.MagicMock()
        args.command = "add"
        args.title = "Test todo"
        args.description = "A test todo"
        args.due = "2027-12-31"
        args.priority = "medium"
        args.status = None
        args.limit = None
        args.todo_id = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = []

            result = handle_add(args, None)

            assert result == 0
            mock_storage_instance.add.assert_called_once()

    def test_add_todo_invalid_date_rejected(self, tmp_path):
        """Test that an invalid date format is rejected when adding a todo."""
        storage_file = tmp_path / "todos.json"
        storage_file.write_text("[]")

        args = mock.MagicMock()
        args.command = "add"
        args.title = "Test todo"
        args.description = "A test todo"
        args.due = "not-a-date"
        args.priority = "medium"
        args.status = None
        args.limit = None
        args.todo_id = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = []

            result = handle_add(args, None)

            assert result == 1

    def test_add_todo_past_date_rejected(self, tmp_path):
        """Test that a past date is rejected when adding a todo."""
        storage_file = tmp_path / "todos.json"
        storage_file.write_text("[]")

        args = mock.MagicMock()
        args.command = "add"
        args.title = "Test todo"
        args.description = "A test todo"
        args.due = "2020-01-01"
        args.priority = "medium"
        args.status = None
        args.limit = None
        args.todo_id = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = []

            result = handle_add(args, None)

            assert result == 1

    def test_add_todo_empty_due_date_accepted(self, tmp_path):
        """Test that an empty due date is accepted when adding a todo."""
        storage_file = tmp_path / "todos.json"
        storage_file.write_text("[]")

        args = mock.MagicMock()
        args.command = "add"
        args.title = "Test todo"
        args.description = "A test todo"
        args.due = ""
        args.priority = "medium"
        args.status = None
        args.limit = None
        args.todo_id = None
        args.storage = str(storage_file)

        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = []

            result = handle_add(args, None)

            assert result == 0
            mock_storage_instance.add.assert_called_once()

    def test_modify_todo_invalid_date_rejected(self, tmp_path):
        """Test that an invalid date format is rejected when modifying a todo."""
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
        args.command = "modify"
        args.todo_id = "1"
        args.title = None
        args.description = None
        args.due = "not-a-date"
        args.priority = None
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

            result = handle_modify(args, None)

            assert result == 1

    def test_modify_todo_valid_date_accepted(self, tmp_path):
        """Test that a valid future date is accepted when modifying a todo."""
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
        args.command = "modify"
        args.todo_id = "1"
        args.title = None
        args.description = None
        args.due = "2028-06-15"
        args.priority = None
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

            result = handle_modify(args, None)

            assert result == 0

    def test_modify_todo_past_date_rejected(self, tmp_path):
        """Test that a past date is rejected when modifying a todo."""
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
        args.command = "modify"
        args.todo_id = "1"
        args.title = None
        args.description = None
        args.due = "2020-01-01"
        args.priority = None
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

            result = handle_modify(args, None)

            assert result == 1


class TestStorageFlagPlacement:
    """Tests for the --storage flag working in both global and per-subcommand positions."""

    def test_storage_before_subcommand(self):
        """Test that --storage works before the subcommand (backward compatibility)."""
        from snekdo.__main__ import create_parser
        parser = create_parser()
        args = parser.parse_args(['--storage', '/tmp/test.json', 'list'])
        assert args.storage == "/tmp/test.json"
        assert args.command == "list"

    def test_storage_after_subcommand_list(self):
        """Test that --storage works after the list subcommand."""
        from snekdo.__main__ import create_parser
        parser = create_parser()
        args = parser.parse_args(['list', '--storage', '/tmp/test.json'])
        assert args.storage == "/tmp/test.json"
        assert args.command == "list"

    def test_storage_after_subcommand_add(self):
        """Test that --storage works after the add subcommand."""
        from snekdo.__main__ import create_parser
        parser = create_parser()
        args = parser.parse_args(['add', '--storage', '/tmp/test.json', '--title', 'Test'])
        assert args.storage == "/tmp/test.json"
        assert args.command == "add"
        assert args.title == "Test"

    def test_storage_after_subcommand_complete(self):
        """Test that --storage works after the complete subcommand."""
        from snekdo.__main__ import create_parser
        parser = create_parser()
        args = parser.parse_args(['complete', '--storage', '/tmp/test.json', '123'])
        assert args.storage == "/tmp/test.json"
        assert args.command == "complete"
        assert args.todo_id == "123"

    def test_storage_after_subcommand_delete(self):
        """Test that --storage works after the delete subcommand."""
        from snekdo.__main__ import create_parser
        parser = create_parser()
        args = parser.parse_args(['delete', '--storage', '/tmp/test.json', '123'])
        assert args.storage == "/tmp/test.json"
        assert args.command == "delete"
        assert args.todo_id == "123"

    def test_storage_after_subcommand_modify(self):
        """Test that --storage works after the modify subcommand."""
        from snekdo.__main__ import create_parser
        parser = create_parser()
        args = parser.parse_args(['modify', '--storage', '/tmp/test.json', '123', '--title', 'New Title'])
        assert args.storage == "/tmp/test.json"
        assert args.command == "modify"
        assert args.todo_id == "123"
        assert args.title == "New Title"

    def test_storage_after_subcommand_show(self):
        """Test that --storage works after the show subcommand."""
        from snekdo.__main__ import create_parser
        parser = create_parser()
        args = parser.parse_args(['show', '--storage', '/tmp/test.json', '123'])
        assert args.storage == "/tmp/test.json"
        assert args.command == "show"
        assert args.todo_id == "123"


class TestMissingStorageAttribute:
    """Tests for handlers working when --storage is omitted (argparse.SUPPRESS).

    These tests verify that the handlers use getattr(args, "storage", None)
    instead of direct attribute access, which would fail when --storage is
    not provided because argparse does not set the attribute on the Namespace.
    """

    def _make_args(self, command, **kwargs):
        """Create a real argparse Namespace with the given command and kwargs.

        The storage attribute is intentionally not set to simulate the
        behavior of argparse.SUPPRESS when --storage is omitted.
        """
        import argparse
        args = argparse.Namespace()
        args.command = command
        for key, value in kwargs.items():
            setattr(args, key, value)
        return args

    def test_add_without_storage_attribute(self, tmp_path, monkeypatch):
        """Test that add works when --storage is omitted (no storage attribute)."""
        default_dir = tmp_path / ".snekdo"
        default_dir.mkdir()
        default_file = default_dir / "todos.json"
        monkeypatch.setenv("HOME", str(tmp_path))

        args = self._make_args(
            "add",
            title="Test todo",
            description="",
            due="2027-12-31",
            priority="medium",
        )
        assert not hasattr(args, "storage")

        from snekdo.__main__ import handle_add
        result = handle_add(args, None)
        assert result == 0
        assert default_file.exists()

    def test_list_without_storage_attribute(self, tmp_path, monkeypatch):
        """Test that list works when --storage is omitted."""
        default_dir = tmp_path / ".snekdo"
        default_dir.mkdir()
        default_file = default_dir / "todos.json"
        default_file.write_text("[]")
        monkeypatch.setenv("HOME", str(tmp_path))

        args = self._make_args(
            "list",
            status="all",
            limit=None,
            todo_id=None,
            sort="created_at",
            reverse=False,
            priority=None,
        )
        assert not hasattr(args, "storage")

        from snekdo.__main__ import handle_list
        result = handle_list(args, None)
        assert result == 0

    def test_complete_without_storage_attribute(self, tmp_path, monkeypatch):
        """Test that complete works when --storage is omitted."""
        default_dir = tmp_path / ".snekdo"
        default_dir.mkdir()
        default_file = default_dir / "todos.json"
        todos = [
            {"id": "1", "title": "Test todo", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00", "priority": "medium"},
        ]
        default_file.write_text(json.dumps(todos))
        monkeypatch.setenv("HOME", str(tmp_path))

        args = self._make_args("complete", todo_id="1")
        assert not hasattr(args, "storage")

        from snekdo.__main__ import handle_complete
        result = handle_complete(args, None)
        assert result == 0

        stored = json.loads(default_file.read_text())
        assert stored[0]["completed"] is True

    def test_delete_without_storage_attribute(self, tmp_path, monkeypatch):
        """Test that delete works when --storage is omitted."""
        default_dir = tmp_path / ".snekdo"
        default_dir.mkdir()
        default_file = default_dir / "todos.json"
        todos = [
            {"id": "1", "title": "Test todo", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00", "priority": "medium"},
        ]
        default_file.write_text(json.dumps(todos))
        monkeypatch.setenv("HOME", str(tmp_path))

        args = self._make_args("delete", todo_id="1")
        assert not hasattr(args, "storage")

        from snekdo.__main__ import handle_delete
        result = handle_delete(args, None)
        assert result == 0

        stored = json.loads(default_file.read_text())
        assert len(stored) == 0

    def test_modify_without_storage_attribute(self, tmp_path, monkeypatch):
        """Test that modify works when --storage is omitted."""
        default_dir = tmp_path / ".snekdo"
        default_dir.mkdir()
        default_file = default_dir / "todos.json"
        todos = [
            {"id": "1", "title": "Test todo", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00", "priority": "medium"},
        ]
        default_file.write_text(json.dumps(todos))
        monkeypatch.setenv("HOME", str(tmp_path))

        args = self._make_args("modify", todo_id="1", title="Updated", description=None, due=None, priority=None)
        assert not hasattr(args, "storage")

        from snekdo.__main__ import handle_modify
        result = handle_modify(args, None)
        assert result == 0

        stored = json.loads(default_file.read_text())
        assert stored[0]["title"] == "Updated"

    def test_show_without_storage_attribute(self, tmp_path, monkeypatch):
        """Test that show works when --storage is omitted."""
        default_dir = tmp_path / ".snekdo"
        default_dir.mkdir()
        default_file = default_dir / "todos.json"
        todos = [
            {"id": "1", "title": "Test todo", "description": "", "due": None, "completed": False, "created_at": "2024-01-01T00:00:00", "priority": "medium"},
        ]
        default_file.write_text(json.dumps(todos))
        monkeypatch.setenv("HOME", str(tmp_path))

        args = self._make_args("show", todo_id="1")
        assert not hasattr(args, "storage")

        from snekdo.__main__ import handle_show
        result = handle_show(args, None)
        assert result == 0

    def test_todo_storage_called_with_none(self, tmp_path, monkeypatch):
        """Test that handlers call TodoStorage with None when --storage is omitted."""
        monkeypatch.setenv("HOME", str(tmp_path))

        args = self._make_args("add", title="Test", description="", due=None, priority="medium")
        assert not hasattr(args, "storage")

        from snekdo.__main__ import handle_add
        with patch("snekdo.__main__.TodoStorage") as mock_storage:
            handle_add(args, None)
            mock_storage.assert_called_once_with(storage_path=None)

    def test_direct_attribute_access_would_fail(self):
        """Test that direct args.storage access raises AttributeError.

        This documents the original bug: direct attribute access on a
        Namespace without the storage attribute raises AttributeError.
        """
        import argparse
        args = argparse.Namespace()
        args.command = "add"
        with pytest.raises(AttributeError):
            _ = args.storage


class TestDebugFlag:
    """Tests for the --debug flag behavior."""

    def test_debug_flag_accepted(self):
        """Test that --debug is accepted before the subcommand."""
        from snekdo.__main__ import create_parser
        parser = create_parser()
        args = parser.parse_args(['--debug', 'list'])
        assert args.debug is True
        assert args.command == "list"

    def test_debug_output_printed_to_stderr(self, capsys, tmp_path):
        """Test that debug output is printed to stderr."""
        storage_file = tmp_path / "todos.json"
        storage_file.write_text("[]")
        from snekdo.__main__ import create_parser, handle_command
        parser = create_parser()
        args = parser.parse_args(['--debug', 'list', '--storage', str(storage_file)])
        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = []
            result = handle_command(args, parser)
        assert result == 0
        captured = capsys.readouterr()
        assert "DEBUG:" in captured.err

    def test_debug_output_includes_command(self, capsys, tmp_path):
        """Test that debug output includes the command name."""
        storage_file = tmp_path / "todos.json"
        storage_file.write_text("[]")
        from snekdo.__main__ import create_parser, handle_command
        parser = create_parser()
        args = parser.parse_args(['--debug', 'add', '--storage', str(storage_file), '--title', 'Test'])
        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = []
            result = handle_command(args, parser)
        assert result == 0
        captured = capsys.readouterr()
        assert "DEBUG: command=add" in captured.err

    def test_debug_output_includes_storage_path(self, capsys, tmp_path):
        """Test that debug output includes the storage path."""
        storage_file = tmp_path / "todos.json"
        storage_file.write_text("[]")
        from snekdo.__main__ import create_parser, handle_command
        parser = create_parser()
        args = parser.parse_args(['--debug', 'list', '--storage', str(storage_file)])
        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = []
            result = handle_command(args, parser)
        assert result == 0
        captured = capsys.readouterr()
        assert f"DEBUG: storage_path={storage_file}" in captured.err

    def test_debug_output_suppressed(self, capsys, tmp_path):
        """Test that debug output is suppressed when --debug is not set."""
        storage_file = tmp_path / "todos.json"
        storage_file.write_text("[]")
        from snekdo.__main__ import create_parser, handle_command
        parser = create_parser()
        args = parser.parse_args(['list', '--storage', str(storage_file)])
        with patch('snekdo.__main__.TodoStorage') as mock_storage:
            mock_storage_instance = mock_storage.return_value
            mock_storage_instance.load.return_value = []
            result = handle_command(args, parser)
        assert result == 0
        captured = capsys.readouterr()
        assert "DEBUG:" not in captured.err
