"""FastAPI REST API for the snekdo todo manager."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from snekdo.api_auth import (
    create_auth_router,
    get_current_user,
    get_current_user_factory,
)
from snekdo.auth import verify_password
from snekdo.due_date import validate_due_date
from snekdo.models import Todo, User
from snekdo.storage import StorageError, TodoStorage, UserStorage

# ---------------------------------------------------------------------------
# Pydantic request / response models
# ---------------------------------------------------------------------------


class TodoCreate(BaseModel):
    """Schema for creating a new todo."""

    title: str = Field(..., min_length=1, max_length=255)
    description: str = ""
    due: str | None = None
    priority: Literal["low", "medium", "high"] = Field(default="medium")

    def to_todo(self) -> Todo:
        """Convert to a :class:`Todo` instance."""
        due = validate_due_date(self.due)
        return Todo(
            title=self.title,
            description=self.description,
            due=due,
            completed=False,
            created_at=datetime.now().isoformat(),
            priority=self.priority,
        )


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo. All fields are optional."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    due: str | None = None
    priority: Literal["low", "medium", "high"] | None = None
    completed: bool | None = None


class TodoResponse(BaseModel):
    """Response model for a single todo."""

    id: str
    title: str
    description: str
    due: str | None
    completed: bool
    created_at: str
    priority: str

    @classmethod
    def from_todo(cls, todo: Todo) -> TodoResponse:
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


class UserUpdate(BaseModel):
    """Schema for updating a user's profile. All fields are optional."""

    display_name: str | None = Field(default=None, max_length=100)
    email: str | None = None


class PasswordChange(BaseModel):
    """Schema for changing a user's password."""

    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)


class UserDeleteConfirm(BaseModel):
    """Schema for confirming account deletion."""

    password: str = Field(..., min_length=1)


class UserProfileResponse(BaseModel):
    """Response model for a user's profile."""

    id: str
    username: str
    display_name: str
    email: str
    created_at: str

    @classmethod
    def from_user(cls, user: User) -> UserProfileResponse:
        return cls(
            id=user.id,
            username=user.username,
            display_name=user.display_name,
            email=user.email,
            created_at=user.created_at,
        )


# ---------------------------------------------------------------------------
# Dependency
# ---------------------------------------------------------------------------


def get_storage(storage_path: str | None = None) -> TodoStorage:
    """Dependency that provides a :class:`TodoStorage` instance."""
    return TodoStorage(storage_path=storage_path)


def _derive_users_path(storage_path: str | None = None) -> str:
    """Derive the users JSON file path from the todos storage path."""
    if storage_path is None:
        return str(Path.home() / ".snekdo" / "users.json")
    path = Path(storage_path)
    if path.name == "todos.json":
        return str(path.with_name("users.json"))
    return str(path.parent / "users.json")


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------


def create_app(storage_path: str | None = None) -> FastAPI:
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

    # Override the default get_current_user to use the correct storage path
    app.dependency_overrides[get_current_user] = get_current_user_factory(
        storage_path=storage_path
    )

    # Include authentication routes (public)
    app.include_router(create_auth_router(storage_path=storage_path))

    @app.get("/api/v1/health", response_model=HealthResponse)
    async def health_check() -> HealthResponse:
        """Health check endpoint."""
        return HealthResponse(status="ok")

    def _get_user_storage() -> UserStorage:
        """Dependency that provides a :class:`UserStorage` instance."""
        return UserStorage(storage_path=_derive_users_path(storage_path))

    @app.get("/api/v1/users/me", response_model=UserProfileResponse)
    async def get_user_profile(
        user_storage: UserStorage = Depends(_get_user_storage),
        current_user: User = Depends(get_current_user),
    ) -> UserProfileResponse:
        """Get the current authenticated user's profile."""
        profile = user_storage.get_profile(current_user.id)
        if profile is None:
            raise HTTPException(
                status_code=404,
                detail=f"User profile not found for ID '{current_user.id}'",
            )
        return UserProfileResponse.from_user(profile)

    @app.put("/api/v1/users/me", response_model=UserProfileResponse)
    async def update_user_profile(
        update_data: UserUpdate,
        user_storage: UserStorage = Depends(_get_user_storage),
        current_user: User = Depends(get_current_user),
    ) -> UserProfileResponse:
        """Update the current authenticated user's profile."""
        display_name = (
            update_data.display_name if update_data.display_name is not None else None
        )
        email = update_data.email if update_data.email is not None else None

        success = user_storage.update_profile(
            current_user.id,
            display_name=display_name,
            email=email,
        )
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"User profile not found for ID '{current_user.id}'",
            )

        profile = user_storage.get_profile(current_user.id)
        if profile is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to retrieve updated profile",
            )
        return UserProfileResponse.from_user(profile)

    @app.put("/api/v1/users/me/password", response_model=MessageResponse)
    async def change_user_password(
        password_data: PasswordChange,
        user_storage: UserStorage = Depends(_get_user_storage),
        current_user: User = Depends(get_current_user),
    ) -> MessageResponse:
        """Change the current authenticated user's password."""
        # Validate that new password and confirm password match
        if password_data.new_password != password_data.confirm_password:
            raise HTTPException(
                status_code=422,
                detail="New password and confirm password do not match",
            )

        try:
            success = user_storage.update_password(
                current_user.id,
                current_password=password_data.current_password,
                new_password=password_data.new_password,
            )
        except StorageError as e:
            raise HTTPException(
                status_code=401,
                detail=str(e),
            ) from e

        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"User profile not found for ID '{current_user.id}'",
            )

        return MessageResponse(message="Password updated successfully")

    @app.delete("/api/v1/users/me", response_model=MessageResponse)
    async def delete_user_account(
        delete_data: UserDeleteConfirm,
        user_storage: UserStorage = Depends(_get_user_storage),
        todo_storage: TodoStorage = Depends(_storage),
        current_user: User = Depends(get_current_user),
    ) -> MessageResponse:
        """Delete the current authenticated user's account.

        Verifies the user's password, deletes all todos belonging to the user,
        and removes the user record.
        """
        # Verify the user's password
        if not verify_password(delete_data.password, current_user.password_hash):
            raise HTTPException(
                status_code=401,
                detail="Incorrect password",
            )

        # Delete the user and all their todos
        success = user_storage.delete_user_with_todos(current_user.id, todo_storage)
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to delete user account",
            )

        return MessageResponse(message="Account deleted successfully")

    @app.get("/api/v1/todos", response_model=list[TodoResponse])
    async def list_todos(
        storage: TodoStorage = Depends(_storage),
        current_user: User = Depends(get_current_user),
        status: str = Query(default="pending", enum=["all", "pending", "completed"]),
        priority: str | None = Query(default=None, enum=["low", "medium", "high"]),
        sort: str | None = Query(
            default="created_at", enum=["created_at", "title", "priority", "completed"]
        ),
        reverse: bool = False,
        limit: int | None = Query(default=None, ge=1),
    ) -> list[TodoResponse]:
        """List all todos, optionally filtered and sorted."""
        todos = storage.load(user_id=current_user.id)

        if status == "pending":
            todos = [t for t in todos if not t.completed]
        elif status == "completed":
            todos = [t for t in todos if t.completed]

        if priority is not None:
            todos = [t for t in todos if t.priority == priority]

        valid_sort_fields = {"created_at", "title", "priority", "completed"}
        if sort in valid_sort_fields:
            if sort == "created_at":
                todos = sorted(
                    todos,
                    key=lambda x: _parse_created_at(x.created_at),
                    reverse=reverse,
                )
            elif sort == "title":
                todos = sorted(todos, key=lambda x: x.title.lower(), reverse=reverse)
            elif sort == "priority":
                priority_order = {"high": 0, "medium": 1, "low": 2}
                todos = sorted(
                    todos,
                    key=lambda x: priority_order.get(x.priority, 1),
                    reverse=reverse,
                )
            elif sort == "completed":
                todos = sorted(todos, key=lambda x: x.completed, reverse=reverse)

        if limit is not None:
            todos = todos[:limit]

        return [TodoResponse.from_todo(t) for t in todos]

    @app.get("/api/v1/todos/{todo_id}", response_model=TodoResponse)
    async def show_todo(
        todo_id: str,
        storage: TodoStorage = Depends(_storage),
        current_user: User = Depends(get_current_user),
    ) -> TodoResponse:
        """Show a single todo by ID."""
        todo = storage.get(todo_id, user_id=current_user.id)
        if todo is None:
            raise HTTPException(
                status_code=404, detail=f"Todo with ID '{todo_id}' not found"
            )
        return TodoResponse.from_todo(todo)

    @app.post("/api/v1/todos", response_model=TodoResponse, status_code=201)
    async def add_todo(
        todo_data: TodoCreate,
        storage: TodoStorage = Depends(_storage),
        current_user: User = Depends(get_current_user),
    ) -> TodoResponse:
        """Add a new todo."""
        try:
            todo = todo_data.to_todo()
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
        todo.user_id = current_user.id
        storage.add(todo)
        return TodoResponse.from_todo(todo)

    @app.post("/api/v1/todos/{todo_id}/complete", response_model=TodoResponse)
    async def complete_todo(
        todo_id: str,
        storage: TodoStorage = Depends(_storage),
        current_user: User = Depends(get_current_user),
    ) -> TodoResponse:
        """Mark a todo as complete."""
        todo = storage.get(todo_id, user_id=current_user.id)
        if todo is None:
            raise HTTPException(
                status_code=404, detail=f"Todo with ID '{todo_id}' not found"
            )
        storage.complete(todo_id, user_id=current_user.id)
        todo.completed = True
        return TodoResponse.from_todo(todo)

    @app.put("/api/v1/todos/{todo_id}", response_model=TodoResponse)
    async def modify_todo(
        todo_id: str,
        update_data: TodoUpdate,
        storage: TodoStorage = Depends(_storage),
        current_user: User = Depends(get_current_user),
    ) -> TodoResponse:
        """Modify an existing todo."""
        todo = storage.get(todo_id, user_id=current_user.id)
        if todo is None:
            raise HTTPException(
                status_code=404, detail=f"Todo with ID '{todo_id}' not found"
            )

        update_dict = {}
        if update_data.title is not None:
            update_dict["title"] = update_data.title
        if update_data.description is not None:
            update_dict["description"] = update_data.description
        if update_data.due is not None and update_data.due.strip() != "":
            try:
                update_dict["due"] = validate_due_date(update_data.due)
            except ValueError as e:
                raise HTTPException(status_code=422, detail=str(e))
        if update_data.priority is not None:
            update_dict["priority"] = update_data.priority
        if update_data.completed is not None:
            update_dict["completed"] = update_data.completed

        if not update_dict:
            # An empty or whitespace-only `due` value is treated as "not provided"
            # (see the due check above), but the request is still valid and the
            # existing todo should be returned with 200.
            if update_data.due is not None:
                pass
            else:
                raise HTTPException(status_code=422, detail="No fields to update")

        storage.modify(todo_id, user_id=current_user.id, **update_dict)
        todo = storage.get(todo_id, user_id=current_user.id)
        return TodoResponse.from_todo(todo)

    @app.delete("/api/v1/todos/{todo_id}", response_model=MessageResponse)
    async def delete_todo(
        todo_id: str,
        storage: TodoStorage = Depends(_storage),
        current_user: User = Depends(get_current_user),
    ) -> MessageResponse:
        """Delete a todo."""
        todo = storage.get(todo_id, user_id=current_user.id)
        if todo is None:
            raise HTTPException(
                status_code=404, detail=f"Todo with ID '{todo_id}' not found"
            )
        storage.delete(todo_id, user_id=current_user.id)
        return MessageResponse(message=f"Deleted todo: {todo.title}")

    return app


# ---------------------------------------------------------------------------
# Helpers (mirroring __main__.py)
# ---------------------------------------------------------------------------


def _parse_created_at(created_at: str) -> datetime:
    """Parse a created_at ISO 8601 string into a datetime object."""
    if not created_at:
        return datetime.min
    try:
        return datetime.fromisoformat(created_at)
    except (ValueError, TypeError):
        return datetime.min
