"""FastAPI REST API for the snekdo todo manager."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from snekdo.models import Todo
from snekdo.storage import StorageError, TodoStorage


# ---------------------------------------------------------------------------
# Pydantic request / response models
# ---------------------------------------------------------------------------

class TodoCreate(BaseModel):
    """Schema for creating a new todo."""

    title: str = Field(..., min_length=1, max_length=255)
    description: str = ""
    due: Optional[str] = None
    priority: str = "medium"

    def to_todo(self) -> Todo:
        """Convert to a :class:`Todo` instance."""
        return Todo(
            title=self.title,
            description=self.description,
            due=self.due or "",
            completed=False,
            created_at=datetime.now().isoformat(),
            priority=self.priority,
        )


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo. All fields are optional."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    due: Optional[str] = None
    priority: Optional[str] = None


class TodoResponse(BaseModel):
    """Response model for a single todo."""

    id: str
    title: str
    description: str
    due: Optional[str]
    completed: bool
    created_at: str
    priority: str

    @classmethod
    def from_todo(cls, todo: Todo) -> "TodoResponse":
        return cls(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            due=todo.due,
            completed=todo.completed,
            created_at=todo.created_at,
            priority=todo.priority,
        )


class HealthResponse(BaseModel):
    """Response for the health-check endpoint."""

    status: str


class MessageResponse(BaseModel):
    """Generic message response."""

    message: str


# ---------------------------------------------------------------------------
# Dependency
# ---------------------------------------------------------------------------

def get_storage(storage_path: Optional[str] = None) -> TodoStorage:
    """Dependency that provides a :class:`TodoStorage` instance."""
    return TodoStorage(storage_path=storage_path)


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

def create_app(storage_path: Optional[str] = None) -> FastAPI:
    """Create the FastAPI application.

    Args:
        storage_path: Optional path to the JSON storage file. If ``None``, the
            default ``~/.snekdo/todos.json`` is used.
    """
    app = FastAPI(
        title="snekdo",
        description="A simple CLI todo list manager with a REST API.",
        version="0.1.0",
    )

    def _storage() -> TodoStorage:
        return get_storage(storage_path)

    @app.get("/api/v1/health", response_model=HealthResponse)
    async def health_check() -> HealthResponse:
        """Health check endpoint."""
        return HealthResponse(status="ok")

    @app.get("/api/v1/todos", response_model=list[TodoResponse])
    async def list_todos(
        storage: TodoStorage = Depends(_storage),
        status: Optional[str] = Query(default=None, enum=["all", "pending", "completed"]),
        priority: Optional[str] = Query(default=None, enum=["low", "medium", "high"]),
        sort: Optional[str] = Query(default="created_at", enum=["created_at", "title", "priority", "completed"]),
        reverse: bool = False,
        limit: Optional[int] = Query(default=None, ge=1),
    ) -> list[TodoResponse]:
        """List all todos, optionally filtered and sorted."""
        todos = storage.load()

        if status == "pending":
            todos = [t for t in todos if not t.completed]
        elif status == "completed":
            todos = [t for t in todos if t.completed]

        if priority is not None:
            todos = [t for t in todos if t.priority == priority]

        valid_sort_fields = {"created_at", "title", "priority", "completed"}
        if sort in valid_sort_fields:
            if sort == "created_at":
                todos = sorted(todos, key=lambda x: _parse_created_at(x.created_at), reverse=reverse)
            elif sort == "title":
                todos = sorted(todos, key=lambda x: x.title.lower(), reverse=reverse)
            elif sort == "priority":
                priority_order = {"high": 0, "medium": 1, "low": 2}
                todos = sorted(todos, key=lambda x: priority_order.get(x.priority, 1), reverse=reverse)
            elif sort == "completed":
                todos = sorted(todos, key=lambda x: x.completed, reverse=reverse)

        if limit is not None:
            todos = todos[:limit]

        return [TodoResponse.from_todo(t) for t in todos]

    @app.get("/api/v1/todos/{todo_id}", response_model=TodoResponse)
    async def show_todo(
        todo_id: str,
        storage: TodoStorage = Depends(_storage),
    ) -> TodoResponse:
        """Show a single todo by ID."""
        todo = storage.get(todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail=f"Todo with ID '{todo_id}' not found")
        return TodoResponse.from_todo(todo)

    @app.post("/api/v1/todos", response_model=TodoResponse, status_code=201)
    async def add_todo(
        todo_data: TodoCreate,
        storage: TodoStorage = Depends(_storage),
    ) -> TodoResponse:
        """Add a new todo."""
        try:
            due = _validate_due_date(todo_data.due) if todo_data.due else ""
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
        todo = todo_data.to_todo()
        todo.due = due
        storage.add(todo)
        return TodoResponse.from_todo(todo)

    @app.post("/api/v1/todos/{todo_id}/complete", response_model=TodoResponse)
    async def complete_todo(
        todo_id: str,
        storage: TodoStorage = Depends(_storage),
    ) -> TodoResponse:
        """Mark a todo as complete."""
        todo = storage.get(todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail=f"Todo with ID '{todo_id}' not found")
        storage.complete(todo_id)
        todo.completed = True
        return TodoResponse.from_todo(todo)

    @app.put("/api/v1/todos/{todo_id}", response_model=TodoResponse)
    async def modify_todo(
        todo_id: str,
        update_data: TodoUpdate,
        storage: TodoStorage = Depends(_storage),
    ) -> TodoResponse:
        """Modify an existing todo."""
        todo = storage.get(todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail=f"Todo with ID '{todo_id}' not found")

        update_dict = {}
        if update_data.title is not None:
            update_dict["title"] = update_data.title
        if update_data.description is not None:
            update_dict["description"] = update_data.description
        if update_data.due is not None:
            try:
                update_dict["due"] = _validate_due_date(update_data.due)
            except ValueError as e:
                raise HTTPException(status_code=422, detail=str(e))
        if update_data.priority is not None:
            update_dict["priority"] = update_data.priority

        if not update_dict:
            raise HTTPException(status_code=422, detail="No fields to update")

        storage.modify(todo_id, **update_dict)
        todo = storage.get(todo_id)
        return TodoResponse.from_todo(todo)

    @app.delete("/api/v1/todos/{todo_id}", response_model=MessageResponse)
    async def delete_todo(
        todo_id: str,
        storage: TodoStorage = Depends(_storage),
    ) -> MessageResponse:
        """Delete a todo."""
        todo = storage.get(todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail=f"Todo with ID '{todo_id}' not found")
        storage.delete(todo_id)
        return MessageResponse(message=f"Deleted todo: {todo.title}")

    return app


# ---------------------------------------------------------------------------
# Helpers (mirroring __main__.py)
# ---------------------------------------------------------------------------

def _validate_due_date(due_date: str) -> str:
    """Validate a due date string (YYYY-MM-DD format)."""
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
    """Parse a created_at ISO 8601 string into a datetime object."""
    if not created_at:
        return datetime.min
    try:
        return datetime.fromisoformat(created_at)
    except (ValueError, TypeError):
        return datetime.min
