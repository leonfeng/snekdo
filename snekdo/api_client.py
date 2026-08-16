"""HTTP client for communicating with the snekdo FastAPI server."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path


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


CREDENTIALS_PATH = Path.home() / ".snekdo" / "credentials.json"


def _read_credentials(credentials_path: Path | None = None) -> dict | None:
    """Read the stored credentials from disk.

    Args:
        credentials_path: Path to the credentials file.
        Defaults to ``~/.snekdo/credentials.json``.

    Returns:
        The credentials dict with ``access_token`` and ``token_type``,
        or ``None`` if the file does not exist.
    """
    if credentials_path is None:
        credentials_path = CREDENTIALS_PATH
    if not credentials_path.exists():
        return None
    with open(credentials_path) as f:
        return json.load(f)


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
        data: dict | None = None,
        credentials_path: Path | None = None,
    ) -> dict:
        """Send an HTTP request to the server.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            path: URL path (without base URL).
            data: Optional JSON body data.
            credentials_path: Optional path to the credentials file.

        Returns:
            The JSON response body as a dict.

        Raises:
            ServerError: If the server returns a non-2xx status.
            ConnectionError: If the connection fails.
            AuthenticationError: If the server returns 401 or 403.
        """
        url = f"{self.base_url}{path}"
        body = None
        headers = {"Content-Type": "application/json"}

        # Include authentication token if available
        credentials = _read_credentials(credentials_path)
        if credentials is not None:
            token = credentials.get("access_token")
            token_type = credentials.get("token_type", "bearer")
            if token:
                headers["Authorization"] = f"{token_type} {token}"

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
            if e.code in (401, 403):
                raise AuthenticationError(
                    f"Authentication failed: {e.code} "
                    f"{'Unauthorized' if e.code == 401 else 'Forbidden'}"
                ) from e
            raise ServerError(f"Server returned status {e.code}: {body_text}") from e
        except urllib.error.URLError as e:
            raise ConnectionError(f"Failed to connect to server: {e}") from e
        except Exception as e:
            raise ConnectionError(f"Connection error: {e}") from e

    def get_todos(self, credentials_path: Path | None = None) -> list[dict]:
        """Fetch all todos from the server.

        Args:
            credentials_path: Optional path to the credentials file.

        Returns:
            A list of todo dicts.
        """
        return self._request("GET", "/api/v1/todos", credentials_path=credentials_path)

    def get_todo(self, todo_id: str, credentials_path: Path | None = None) -> dict:
        """Fetch a single todo by ID.

        Args:
            todo_id: The ID of the todo.
            credentials_path: Optional path to the credentials file.

        Returns:
            The todo dict.

        Raises:
            ServerError: If the todo is not found.
        """
        return self._request(
            "GET", f"/api/v1/todos/{todo_id}", credentials_path=credentials_path
        )

    def create_todo(
        self,
        title: str,
        description: str = "",
        due: str | None = None,
        priority: str = "medium",
        credentials_path: Path | None = None,
    ) -> dict:
        """Create a new todo on the server.

        Args:
            title: The title of the todo.
            description: The description of the todo.
            due: The due date (YYYY-MM-DD format).
            priority: The priority level (low, medium, high).
            credentials_path: Optional path to the credentials file.

        Returns:
            The created todo dict.
        """
        data: dict = {"title": title, "description": description, "priority": priority}
        if due:
            data["due"] = due
        return self._request(
            "POST", "/api/v1/todos", data=data, credentials_path=credentials_path
        )

    def update_todo(
        self,
        todo_id: str,
        title: str | None = None,
        description: str | None = None,
        due: str | None = None,
        priority: str | None = None,
        credentials_path: Path | None = None,
    ) -> dict:
        """Update an existing todo on the server.

        Args:
            todo_id: The ID of the todo.
            title: New title.
            description: New description.
            due: New due date.
            priority: New priority.
            credentials_path: Optional path to the credentials file.

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
        return self._request(
            "PUT",
            f"/api/v1/todos/{todo_id}",
            data=data,
            credentials_path=credentials_path,
        )

    def delete_todo(self, todo_id: str, credentials_path: Path | None = None) -> dict:
        """Delete a todo on the server.

        Args:
            todo_id: The ID of the todo.
            credentials_path: Optional path to the credentials file.

        Returns:
            The message response dict.
        """
        return self._request(
            "DELETE", f"/api/v1/todos/{todo_id}", credentials_path=credentials_path
        )

    def complete_todo(self, todo_id: str, credentials_path: Path | None = None) -> dict:
        """Mark a todo as complete on the server.

        Args:
            todo_id: The ID of the todo.
            credentials_path: Optional path to the credentials file.

        Returns:
            The updated todo dict.
        """
        return self._request(
            "POST",
            f"/api/v1/todos/{todo_id}/complete",
            credentials_path=credentials_path,
        )

    def get_profile(self, credentials_path: Path | None = None) -> dict:
        """Get the current user's profile.

        Args:
            credentials_path: Optional path to the credentials file.

        Returns:
            The user profile dict.
        """
        return self._request(
            "GET", "/api/v1/users/me", credentials_path=credentials_path
        )

    def update_profile(
        self,
        display_name: str | None = None,
        email: str | None = None,
        credentials_path: Path | None = None,
    ) -> dict:
        """Update the current user's profile.

        Args:
            display_name: New display name.
            email: New email.
            credentials_path: Optional path to the credentials file.

        Returns:
            The updated user profile dict.
        """
        data: dict = {}
        if display_name is not None:
            data["display_name"] = display_name
        if email is not None:
            data["email"] = email
        return self._request(
            "PUT", "/api/v1/users/me", data=data, credentials_path=credentials_path
        )

    def change_password(
        self,
        current_password: str,
        new_password: str,
        confirm_password: str,
        credentials_path: Path | None = None,
    ) -> dict:
        """Change the current user's password.

        Args:
            current_password: The current password.
            new_password: The new password.
            confirm_password: The new password confirmation.
            credentials_path: Optional path to the credentials file.

        Returns:
            The message response dict.
        """
        data = {
            "current_password": current_password,
            "new_password": new_password,
            "confirm_password": confirm_password,
        }
        return self._request(
            "PUT",
            "/api/v1/users/me/password",
            data=data,
            credentials_path=credentials_path,
        )

    def delete_account(
        self, password: str, credentials_path: Path | None = None
    ) -> dict:
        """Delete the current user's account.

        Args:
            password: The user's current password for confirmation.
            credentials_path: Optional path to the credentials file.

        Returns:
            The message response dict.

        Raises:
            AuthenticationError: If the password is incorrect.
        """
        data = {"password": password}
        return self._request(
            "DELETE", "/api/v1/users/me", data=data, credentials_path=credentials_path
        )


class ServerError(Exception):
    """Raised when the server returns an error response."""


class ConnectionError(Exception):
    """Raised when the client cannot connect to the server."""


class AuthenticationError(Exception):
    """Raised when authentication fails (401/403)."""
