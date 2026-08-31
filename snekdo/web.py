"""Jinja2 + HTMX web frontend for the snekdo todo manager."""

from __future__ import annotations

import re
from pathlib import Path

from fastapi import Depends, FastAPI, Form, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from jinja2 import Environment, FileSystemLoader

from snekdo.api import TodoCreate
from snekdo.auth import decode_access_token, verify_password
from snekdo.csrf import (
    delete_csrf_token_cookie,
    get_csrf_token_cookie,
    verify_csrf_token,
)
from snekdo.due_date import validate_due_date
from snekdo.models import Todo, User
from snekdo.storage import StorageError, TodoStorage, UserStorage
from snekdo.web_auth import register_web_routes as register_auth_web_routes

EMAIL_REGEX = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')


def get_user_storage(storage_path: str | None = None) -> UserStorage:
    """Dependency that provides a :class:`UserStorage` instance."""
    if storage_path is None:
        return UserStorage()
    path = Path(storage_path)
    return UserStorage(storage_path=str(path.with_name("users.json")))


def get_template_env() -> Environment:
    """Create a Jinja2 environment with the templates directory."""
    templates_dir = Path(__file__).parent / "templates"
    return Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )


def get_storage(storage_path: str | None = None) -> TodoStorage:
    """Dependency that provides a :class:`TodoStorage` instance."""
    return TodoStorage(storage_path=storage_path)


def _filter_todos(
    todos: list[Todo],
    q: str | None = None,
    status: str = "pending",
    priority: str | None = None,
) -> list[Todo]:
    """Filter todos by search query, status, and priority (AND semantics)."""
    if q:
        q_lower = q.lower()
        todos = [
            t for t in todos
            if q_lower in t.title.lower() or q_lower in (t.description or "").lower()
        ]
    if status == "pending":
        todos = [t for t in todos if not t.completed]
    elif status == "completed":
        todos = [t for t in todos if t.completed]
    if priority:
        todos = [t for t in todos if t.priority == priority]
    return todos


def _render(request: Request, template_name: str, **context) -> Response:
    """Render a Jinja2 template and return an HTML response.

    Automatically includes the CSRF token in the template context so that
    forms can include it as a hidden input.
    """
    csrf_token = get_csrf_token_cookie(request)
    context.setdefault("csrf_token", csrf_token)
    template = request.app.state.template_env.get_template(template_name)
    return Response(template.render(**context), media_type="text/html")


def register_web_routes(app: FastAPI, storage_path: str | None = None) -> None:
    """Register web routes on the given FastAPI app.

    This adds Jinja2-rendered web pages alongside the REST API routes so that
    a single ``snekdo serve`` process serves both the API and the web UI.
    """

    if not hasattr(app.state, "template_env") or app.state.template_env is None:
        app.state.template_env = get_template_env()

    def _storage(request: Request) -> TodoStorage:
        return get_storage(storage_path)

    def _require_login(
        request: Request,
    ) -> str:
        """Require a logged-in user and return their user_id.

        The token is read from the token cookie. If no token is present,
        the user is redirected to the login page.
        """
        token = request.cookies.get("token")
        if token is None:
            raise HTTPException(
                status_code=302, headers={"location": "/auth/login"}
            )

        user_id = decode_access_token(token)
        if user_id is None:
            raise HTTPException(
                status_code=302, headers={"location": "/auth/login"}
            )

        user_storage = get_user_storage(storage_path)
        user = user_storage.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=302, headers={"location": "/auth/login"}
            )

        return user_id

    # ------------------------------------------------------------------
    # List todos
    # ------------------------------------------------------------------

    @app.get("/")
    async def index(
        request: Request,
        q: str | None = None,
        status: str = "pending",
        priority: str | None = None,
        storage: TodoStorage = Depends(_storage),
        user_id: str = Depends(_require_login),
    ) -> Response:
        """List todos with search and filters (alias for /todos)."""
        todos = _filter_todos(storage.load(user_id=user_id), q, status, priority)
        return _render(
            request,
            "list.html",
            todos=todos,
            q=q or "",
            status=status,
            priority=priority or "",
            title="Todos",
        )

    @app.get("/todos")
    async def list_todos(
        request: Request,
        q: str | None = None,
        status: str = "pending",
        priority: str | None = None,
        storage: TodoStorage = Depends(_storage),
        user_id: str = Depends(_require_login),
    ) -> Response:
        """List todos with search and filters."""
        todos = _filter_todos(storage.load(user_id=user_id), q, status, priority)
        return _render(
            request,
            "list.html",
            todos=todos,
            q=q or "",
            status=status,
            priority=priority or "",
            title="Todos",
        )

    # ------------------------------------------------------------------
    # Add todo (must be before /todos/{todo_id} to avoid path param match)
    # ------------------------------------------------------------------

    @app.get("/todos/add")
    async def show_add_form(
        request: Request,
        user_id: str = Depends(_require_login),
        error: str | None = None,
    ) -> Response:
        """Render the add todo form."""
        return _render(
            request,
            "add.html",
            title="Add Todo",
            error=error,
        )

    def _parse_tags(raw: str) -> list[str]:
        seen: set[str] = set()
        tags: list[str] = []
        for part in raw.split(","):
            tag = part.strip()
            if tag and tag not in seen:
                seen.add(tag)
                tags.append(tag)
        return tags

    @app.post("/todos/add")
    async def add_todo(
        request: Request,
        title: str = Form(default=""),
        description: str = Form(default=""),
        due: str | None = Form(default=""),
        priority: str = Form(default="medium"),
        repeat: str = Form(default="none"),
        tags: str = Form(default=""),
        category: str = Form(default=""),
        storage: TodoStorage = Depends(_storage),
        user_id: str = Depends(_require_login),
    ) -> Response:
        """Create a new todo and redirect to the list."""
        if not await verify_csrf_token(request):
            return _render(
                request,
                "add.html",
                title="Add Todo",
                error="Invalid CSRF token. Please try again.",
            )
        if not title or not title.strip():
            return _render(
                request,
                "add.html",
                title="Add Todo",
                error="Title is required",
            )
        if priority not in ("high", "medium", "low"):
            return _render(
                request,
                "add.html",
                title="Add Todo",
                error="Priority must be high, medium, or low",
            )
        if repeat not in ("none", "daily", "weekly", "monthly", "yearly"):
            return _render(
                request,
                "add.html",
                title="Add Todo",
                error="Repeat must be none, daily, weekly, monthly, or yearly",
            )
        todo_data = TodoCreate(
            title=title,
            description=description,
            due=due,
            priority=priority,
            repeat=repeat,
            tags=_parse_tags(tags),
            category=category or None,
        )
        try:
            todo = todo_data.to_todo()
        except ValueError as e:
            return _render(
                request,
                "add.html",
                title="Add Todo",
                error=str(e),
            )
        except RequestValidationError as e:
            return _render(
                request,
                "add.html",
                title="Add Todo",
                error=str(e.errors()),
            )
        todo.user_id = user_id
        storage.add(todo)
        return RedirectResponse(url="/todos", status_code=302)

    # ------------------------------------------------------------------
    # Edit todo
    # ------------------------------------------------------------------

    @app.get("/todos/{todo_id}/edit")
    async def show_edit_form(
        request: Request,
        todo_id: str,
        storage: TodoStorage = Depends(_storage),
        user_id: str = Depends(_require_login),
    ) -> Response:
        """Render the edit todo form."""
        todo = storage.get(todo_id, user_id=user_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return _render(
            request,
            "edit.html",
            title="Edit Todo",
            todo=todo,
            error=None,
        )

    @app.post("/todos/{todo_id}/edit")
    async def edit_todo(
        request: Request,
        todo_id: str,
        title: str = Form(default=""),
        description: str = Form(default=""),
        due: str | None = Form(default=""),
        priority: str = Form(default="medium"),
        repeat: str = Form(default="none"),
        tags: str = Form(default=""),
        category: str = Form(default=""),
        storage: TodoStorage = Depends(_storage),
        user_id: str = Depends(_require_login),
    ) -> Response:
        """Update an existing todo and redirect to the list."""
        todo = storage.get(todo_id, user_id=user_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        if not await verify_csrf_token(request):
            return _render(
                request,
                "edit.html",
                title="Edit Todo",
                todo=todo,
                error="Invalid CSRF token. Please try again.",
            )
        if not title or not title.strip():
            return _render(
                request,
                "edit.html",
                title="Edit Todo",
                todo=todo,
                error="Title is required",
            )
        if priority not in ("high", "medium", "low"):
            return _render(
                request,
                "edit.html",
                title="Edit Todo",
                todo=todo,
                error="Priority must be high, medium, or low",
            )
        if repeat not in ("none", "daily", "weekly", "monthly", "yearly"):
            return _render(
                request,
                "edit.html",
                title="Edit Todo",
                todo=todo,
                error="Repeat must be none, daily, weekly, monthly, or yearly",
            )
        update_kwargs = {
            "title": title,
            "description": description,
            "priority": priority,
            "repeat": repeat,
            "tags": _parse_tags(tags),
            "category": category or None,
        }
        try:
            due_clean = validate_due_date(due)
        except ValueError as e:
            return _render(
                request,
                "edit.html",
                title="Edit Todo",
                todo=todo,
                error=str(e),
            )
        if due_clean is not None:
            update_kwargs["due"] = due_clean
        elif due == "":
            # Empty string means the user cleared the due date
            update_kwargs["due"] = None
        try:
            storage.modify(todo_id, **update_kwargs)
        except RequestValidationError as e:
            return _render(
                request,
                "edit.html",
                title="Edit Todo",
                todo=todo,
                error=str(e.errors()),
            )
        return RedirectResponse(url="/todos", status_code=302)

    # ------------------------------------------------------------------
    # Complete todo (HTMX or redirect)
    # ------------------------------------------------------------------

    @app.post("/todos/{todo_id}/complete")
    async def complete_todo(
        request: Request,
        todo_id: str,
        storage: TodoStorage = Depends(_storage),
        user_id: str = Depends(_require_login),
    ) -> Response:
        """Mark a todo as complete. Returns partial HTML for HTMX or redirects."""
        if not await verify_csrf_token(request):
            raise HTTPException(status_code=403, detail="Invalid CSRF token")
        todo = storage.get(todo_id, user_id=user_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        storage.complete(todo_id, user_id=user_id)
        # Load the most recent instance to avoid stale object attributes
        todo = storage.get(todo_id, user_id=user_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")

        if request.headers.get("HX-Request"):
            return _render(
                request,
                "list_row.html",
                todo=todo,
                title="Todos",
            )
        return RedirectResponse(url="/todos", status_code=302)

    # ------------------------------------------------------------------
    # Delete todo (HTMX or redirect)
    # ------------------------------------------------------------------

    @app.post("/todos/{todo_id}/delete")
    async def delete_todo(
        request: Request,
        todo_id: str,
        storage: TodoStorage = Depends(_storage),
        user_id: str = Depends(_require_login),
    ) -> Response:
        """Delete a todo. Returns partial HTML for HTMX or redirects."""
        if not await verify_csrf_token(request):
            raise HTTPException(status_code=403, detail="Invalid CSRF token")
        todo = storage.get(todo_id, user_id=user_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        storage.delete(todo_id, user_id=user_id)

        if request.headers.get("HX-Request"):
            todos = storage.load(user_id=user_id)
            pending = [t for t in todos if not t.completed]
            return _render(
                request,
                "list_rows.html",
                todos=pending,
                title="Todos",
            )
        return RedirectResponse(url="/todos", status_code=302)

    # ------------------------------------------------------------------
    # Show todo (must be after /todos/add to avoid path param match)
    # ------------------------------------------------------------------

    @app.get("/todos/{todo_id}")
    async def show_todo(
        request: Request,
        todo_id: str,
        storage: TodoStorage = Depends(_storage),
        user_id: str = Depends(_require_login),
    ) -> Response:
        """Show a single todo's details."""
        todo = storage.get(todo_id, user_id=user_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return _render(request, "show.html", todo=todo, title="Todo Details")

    # ------------------------------------------------------------------
    # Authentication routes
    # ------------------------------------------------------------------

    register_auth_web_routes(router=app, storage_path=storage_path)

    # ------------------------------------------------------------------
    # Profile routes
    # ------------------------------------------------------------------

    @app.get("/profile")
    async def profile_page(
        request: Request,
        user_id: str = Depends(_require_login),
    ) -> Response:
        """Render the user profile page."""
        user_storage = get_user_storage(storage_path)
        user = user_storage.get_profile(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return _render(request, "profile.html", title="Profile", user=user)

    @app.post("/profile/update")
    async def update_profile(
        request: Request,
        display_name: str = Form(default=""),
        email: str = Form(default=""),
        user_id: str = Depends(_require_login),
    ) -> Response:
        """Update the authenticated user's profile."""
        if not await verify_csrf_token(request):
            _user_storage = get_user_storage(storage_path)
            user = _user_storage.get_profile(user_id)
            return _render(
                request,
                "profile_content.html",
                title="Profile",
                user=user or User(username=user_id),
                error="Invalid CSRF token. Please try again.",
            )
        user_storage = get_user_storage(storage_path)
        user = user_storage.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        errors = []
        if email and not EMAIL_REGEX.match(email):
            errors.append("Invalid email format")

        if errors:
            user = user_storage.get_profile(user_id)
            return _render(
                request,
                "profile_content.html",
                title="Profile",
                user=user,
                error="; ".join(errors),
            )

        user_storage.update_profile(
            user_id,
            display_name=display_name,
            email=email,
        )
        user = user_storage.get_profile(user_id)

        if request.headers.get("HX-Request"):
            return _render(request, "profile_content.html", title="Profile", user=user)
        return RedirectResponse(url="/profile", status_code=302)

    @app.post("/profile/password")
    async def change_password(
        request: Request,
        current_password: str = Form(default=""),
        new_password: str = Form(default=""),
        confirm_password: str = Form(default=""),
        user_id: str = Depends(_require_login),
    ) -> Response:
        """Change the authenticated user's password."""
        if not await verify_csrf_token(request):
            user_storage = get_user_storage(storage_path)
            user = user_storage.get_profile(user_id)
            return _render(
                request,
                "profile_content.html",
                title="Profile",
                user=user,
                error="Invalid CSRF token. Please try again.",
            )
        user_storage = get_user_storage(storage_path)
        user = user_storage.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        errors = []
        if not verify_password(current_password, user.password_hash):
            errors.append("Current password is incorrect")
        if len(new_password) < 8:
            errors.append("Password must be at least 8 characters")
        if new_password != confirm_password:
            errors.append("Passwords do not match")

        if errors:
            user = user_storage.get_profile(user_id)
            return _render(
                request,
                "profile_content.html",
                title="Profile",
                user=user,
                error="; ".join(errors),
            )

        try:
            user_storage.update_password(user_id, current_password, new_password)
        except StorageError as e:
            errors.append(str(e))
            user = user_storage.get_profile(user_id)
            return _render(
                request,
                "profile_content.html",
                title="Profile",
                user=user,
                error="; ".join(errors),
            )

        if request.headers.get("HX-Request"):
            user = user_storage.get_profile(user_id)
            return _render(request, "profile_content.html", title="Profile", user=user)
        return RedirectResponse(url="/profile", status_code=302)

    @app.post("/profile/delete")
    async def delete_account(
        request: Request,
        current_password: str = Form(default=""),
        user_id: str = Depends(_require_login),
        storage: TodoStorage = Depends(_storage),
    ) -> Response:
        """Delete the authenticated user's account and show confirmation page."""
        if not await verify_csrf_token(request):
            user_storage = get_user_storage(storage_path)
            user = user_storage.get_profile(user_id)
            return _render(
                request,
                "profile_content.html",
                title="Profile",
                user=user,
                error="Invalid CSRF token. Please try again.",
            )
        user_storage = get_user_storage(storage_path)
        user = user_storage.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        errors = []
        if not verify_password(current_password, user.password_hash):
            errors.append("Incorrect password")
            user = user_storage.get_profile(user_id)
            return _render(
                request,
                "profile_content.html",
                title="Profile",
                user=user,
                error="; ".join(errors),
            )

        # Delete the user and all their todos
        user_storage.delete_user_with_todos(user_id, storage)

        # For HTMX requests, render the confirmation page directly
        if request.headers.get("HX-Request"):
            return _render(request, "confirmation.html", error=None)
        # For regular requests, redirect to confirmation page
        response = RedirectResponse(url="/confirmation", status_code=302)
        response.delete_cookie(key="token")
        return response


def create_web_app(storage_path: str | None = None) -> FastAPI:
    """Create a standalone FastAPI web application with Jinja2 templates.

    Args:
        storage_path: Optional path to the JSON storage file. If ``None``, the
            default ``~/.snekdo/todos.json`` is used.
    """
    app = FastAPI(
        title="snekdo web",
        description="A simple web UI for the snekdo todo list manager.",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
    )
    register_web_routes(app, storage_path=storage_path)
    return app
