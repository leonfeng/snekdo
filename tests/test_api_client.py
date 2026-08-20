"""Tests for the API client layer."""

from unittest.mock import patch

from snekdo.api_client import ServerHttpClient


class TestAPIClient:
    """Test cases for the API client."""

    def test_update_todo_includes_completed_true(self):
        """Test that update_todo includes completed=True in the request body."""
        client = ServerHttpClient(base_url="http://127.0.0.1:8000")

        with patch.object(client, "_request", return_value={"id": "1", "completed": True}) as mock_request:
            client.update_todo(
                todo_id="1",
                title="Updated title",
                completed=True,
            )

            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[1]["data"]["completed"] is True

    def test_update_todo_includes_completed_false(self):
        """Test that update_todo includes completed=False in the request body."""
        client = ServerHttpClient(base_url="http://127.0.0.1:8000")

        with patch.object(client, "_request", return_value={"id": "1", "completed": False}) as mock_request:
            client.update_todo(
                todo_id="1",
                title="Updated title",
                completed=False,
            )

            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[1]["data"]["completed"] is False

    def test_update_todo_omits_completed_when_not_provided(self):
        """Test that update_todo omits the completed key when not provided."""
        client = ServerHttpClient(base_url="http://127.0.0.1:8000")

        with patch.object(client, "_request", return_value={"id": "1", "completed": False}) as mock_request:
            client.update_todo(
                todo_id="1",
                title="Updated title",
            )

            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert "completed" not in call_args[1]["data"]

    def test_update_todo_with_all_fields(self):
        """Test that update_todo includes all provided fields."""
        client = ServerHttpClient(base_url="http://127.0.0.1:8000")

        with patch.object(client, "_request", return_value={"id": "1"}) as mock_request:
            client.update_todo(
                todo_id="1",
                title="New title",
                description="New description",
                due="2025-12-31",
                priority="high",
                completed=True,
            )

            mock_request.assert_called_once()
            call_args = mock_request.call_args
            data = call_args[1]["data"]
            assert data["title"] == "New title"
            assert data["description"] == "New description"
            assert data["due"] == "2025-12-31"
            assert data["priority"] == "high"
            assert data["completed"] is True

    def test_update_todo_put_method(self):
        """Test that update_todo uses the PUT method."""
        client = ServerHttpClient(base_url="http://127.0.0.1:8000")

        with patch.object(client, "_request", return_value={"id": "1"}) as mock_request:
            client.update_todo(todo_id="1", title="Updated title")

            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[0][0] == "PUT"
            assert call_args[0][1] == "/api/v1/todos/1"

    def test_sync_passes_completed_to_update_todo(self):
        """Test that _sync passes the completed field when updating a todo."""
        from snekdo.__main__ import _sync
        from snekdo.models import Todo

        client = ServerHttpClient(base_url="http://127.0.0.1:8000")
        storage_path = "/tmp/test_sync_todos.json"

        # Create a local todo that is completed
        local_todo = Todo(
            id="1",
            title="Test todo",
            description="A test todo",
            due="2025-12-31",
            completed=True,
            created_at="2024-01-01T00:00:00",
            priority="medium",
        )

        with patch.object(client, "get_todos", return_value=[
            {
                "id": "1",
                "title": "Test todo",
                "description": "A test todo",
                "due": "2025-12-31",
                "completed": False,
                "created_at": "2024-01-01T00:00:00",
                "priority": "medium",
            }
        ]):
            with patch.object(client, "update_todo", return_value={
                "id": "1",
                "title": "Test todo",
                "description": "A test todo",
                "due": "2025-12-31",
                "completed": True,
                "created_at": "2024-01-01T00:00:00",
                "priority": "medium",
            }) as mock_update:
                with patch("snekdo.storage.TodoStorage") as mock_storage:
                    mock_storage_instance = mock_storage.return_value
                    mock_storage_instance.load.return_value = [local_todo]
                    mock_storage_instance.save.return_value = None

                    summary = _sync(client, storage_path, "push")

                    assert summary.updated == 1
                    mock_update.assert_called_once()
                    call_args = mock_update.call_args
                    assert call_args[1]["completed"] is True

    def test_sync_passes_completed_false_to_update_todo(self):
        """Test that _sync passes completed=False when updating a todo."""
        from snekdo.__main__ import _sync
        from snekdo.models import Todo

        client = ServerHttpClient(base_url="http://127.0.0.1:8000")
        storage_path = "/tmp/test_sync_todos2.json"

        local_todo = Todo(
            id="1",
            title="Test todo",
            description="A test todo",
            due="2025-12-31",
            completed=False,
            created_at="2024-01-01T00:00:00",
            priority="medium",
        )

        with patch.object(client, "get_todos", return_value=[
            {
                "id": "1",
                "title": "Test todo",
                "description": "A test todo",
                "due": "2025-12-31",
                "completed": True,
                "created_at": "2024-01-01T00:00:00",
                "priority": "medium",
            }
        ]):
            with patch.object(client, "update_todo", return_value={
                "id": "1",
                "title": "Test todo",
                "description": "A test todo",
                "due": "2025-12-31",
                "completed": False,
                "created_at": "2024-01-01T00:00:00",
                "priority": "medium",
            }) as mock_update:
                with patch("snekdo.storage.TodoStorage") as mock_storage:
                    mock_storage_instance = mock_storage.return_value
                    mock_storage_instance.load.return_value = [local_todo]
                    mock_storage_instance.save.return_value = None

                    summary = _sync(client, storage_path, "push")

                    assert summary.updated == 1
                    mock_update.assert_called_once()
                    call_args = mock_update.call_args
                    assert call_args[1]["completed"] is False
