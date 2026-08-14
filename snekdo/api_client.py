"""HTTP client for communicating with the snekdo FastAPI server."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Optional


@dataclass
class SyncSummary:
    """Summary of a sync operation."""

    pulled: int = 0
    pushed: int = 0
    updated: int = 0
    deleted: int = 0
    errors: list[str] | None = None

    def __str__(self) -> str:
        parts = [
            f"pulled={self.pulled}",
            f"pushed={self.pushed}",
            f"updated={self.updated}",
            f"deleted={self.deleted}",
        ]
        if self.errors:
            parts.append(f"errors={len(self.errors)}")
        return "Sync summary: " + ", ".join(parts)


class ServerHttpClient:
    """HTTP client for the snekdo FastAPI server.

    Uses only the Python standard library (``urllib.request``) to avoid
    adding new dependencies.
    """

    def __init__(self, base_url: str = "http://127.0.0.1:8000") -> None:
        """Initialize the HTTP client.

        Args:
            base_url: The base URL of the server, e.g. ``http://127.0.0.1:8000``.
        """
        self.base_url = base_url.rstrip("/")

    def _request(
        self,
        method: str,
        path: str,
        data: Optional[dict] = None,
    ) -> dict:
        """Send an HTTP request to the server.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            path: URL path (without base URL).
            data: Optional JSON body data.

        Returns:
            The JSON response body as a dict.

        Raises:
            ServerError: If the server returns a non-2xx status.
            ConnectionError: If the connection fails.
        """
        url = f"{self.base_url}{path}"
        body = None
        headers = {"Content-Type": "application/json"}

        if data is not None:
            body = json.dumps(data).encode("utf-8")

        request = urllib.request.Request(
            url,
            data=body,
            headers=headers,
            method=method,
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body_text = response.read().decode("utf-8")
                if response.status >= 300:
                    raise ServerError(
                        f"Server returned status {response.status}: {body_text}"
                    )
                if body_text:
                    return json.loads(body_text)
                return {}
        except urllib.error.HTTPError as e:
            body_text = e.read().decode("utf-8") if e.readable() else ""
            raise ServerError(
                f"Server returned status {e.code}: {body_text}"
            ) from e
        except urllib.error.URLError as e:
            raise ConnectionError(f"Failed to connect to server: {e}") from e
        except Exception as e:
            raise ConnectionError(f"Connection error: {e}") from e

    def get_todos(self) -> list[dict]:
        """Fetch all todos from the server.

        Returns:
            A list of todo dicts.
        """
        return self._request("GET", "/api/v1/todos")

    def get_todo(self, todo_id: str) -> dict:
        """Fetch a single todo by ID.

        Args:
            todo_id: The ID of the todo.

        Returns:
            The todo dict.

        Raises:
            ServerError: If the todo is not found.
        """
        return self._request("GET", f"/api/v1/todos/{todo_id}")

    def create_todo(self, title: str, description: str = "", due: Optional[str] = None, priority: str = "medium") -> dict:
        """Create a new todo on the server.

        Args:
            title: The title of the todo.
            description: The description of the todo.
            due: The due date (YYYY-MM-DD format).
            priority: The priority level (low, medium, high).

        Returns:
            The created todo dict.
        """
        data: dict = {"title": title, "description": description, "priority": priority}
        if due:
            data["due"] = due
        return self._request("POST", "/api/v1/todos", data=data)

    def update_todo(self, todo_id: str, title: Optional[str] = None, description: Optional[str] = None, due: Optional[str] = None, priority: Optional[str] = None) -> dict:
        """Update an existing todo on the server.

        Args:
            todo_id: The ID of the todo.
            title: New title.
            description: New description.
            due: New due date.
            priority: New priority.

        Returns:
            The updated todo dict.
        """
        data: dict = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if due is not None:
            data["due"] = due
        if priority is not None:
            data["priority"] = priority
        return self._request("PUT", f"/api/v1/todos/{todo_id}", data=data)

    def delete_todo(self, todo_id: str) -> dict:
        """Delete a todo on the server.

        Args:
            todo_id: The ID of the todo.

        Returns:
            The message response dict.
        """
        return self._request("DELETE", f"/api/v1/todos/{todo_id}")

    def complete_todo(self, todo_id: str) -> dict:
        """Mark a todo as complete on the server.

        Args:
            todo_id: The ID of the todo.

        Returns:
            The updated todo dict.
        """
        return self._request("POST", f"/api/v1/todos/{todo_id}/complete")


class ServerError(Exception):
    """Raised when the server returns an error response."""


class ConnectionError(Exception):
    """Raised when the client cannot connect to the server."""
