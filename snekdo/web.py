"""Jinja2 + HTMX web frontend for the snekdo todo manager."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import Cookie, Depends, FastAPI, Form, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader

from snekdo.auth import decode_access_token
from snekdo.models import Todo
from snekdo.storage import TodoStorage, UserStorage
from snekdo.web_auth import register_web_routes as register_auth_web_routes


def get_user_storage(storage_path: Optional[str] = None) -> UserStorage:
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


def get_storage(storage_path: Optional[str] = None) -> TodoStorage:
    """Dependency that provides a :class:`TodoStorage` instance."""
    return TodoStorage(storage_path=storage_path)


def _render(request: Request, template_name: str, **context) -> Response:
    """Render a Jinja2 template and return an HTML response."""
    template = request.app.state.template_env.get_template(template_name)
    return Response(template.render(**context), media_type="text/html")


def register_web_routes(app: FastAPI, storage_path: Optional[str] = None) -> None:
    """Register web routes on the given FastAPI app.

    This adds Jinja2-rendered web pages alongside the REST API routes so that
    a single ``snekdo serve`` process serves both the API and the web UI.
    """

    if not hasattr(app.state, "template_env") or app.state.template_env is None:
        app.state.template_env = get_template_env()

    def _storage(request: Request) -> TodoStorage:
        return get_storage(storage_path)

    def _validate_due_date(due_date: str) -> str:
        """Validate a due date string (YYYY-MM-DD format)."""
        from snekdo.__main__ import validate_due_date as _v
        return _v(due_date)

    def _require_login(
        request: Request,
        token: Optional[str] = Cookie(default=None),
    ) -> str:
        """Require a logged-in user and return their user_id.

        The token is read from the token cookie. If no token is present,
        the user is redirected to the login page.
        """
        if token is None:
            return RedirectResponse(url="/auth/login", status_code=302)

        user_id = decode_access_token(token)
        if user_id is None:
            return RedirectResponse(url="/auth/login", status_code=302)

        user_storage = get_user_storage(storage_path)
        user = user_storage.get_by_id(user_id)
        if user is None:
            return RedirectResponse(url="/auth/login", status_code=302)

        return user_id

    # ------------------------------------------------------------------
    # List todos
    # ------------------------------------------------------------------

    @app.get("/")
    async def index(
        request: Request,
        storage: TodoStorage = Depends(_storage),
        user_id: str = Depends(_require_login),
    ) -> Response:
        """List pending todos (alias for /todos)."""
        todos = storage.load(user_id=user_id)
        pending = [t for t in todos if not t.completed]
        return _render(request, "list.html", todos=pending, title="Todos")

    @app.get("/todos")
    async def list_todos(
        request: Request,
        storage: TodoStorage = Depends(_storage),
        user_id: str = Depends(_require_login),
    ) -> Response:
        """List pending todos."""
        todos = storage.load(user_id=user_id)
        pending = [t for t in todos if not t.completed]
        return _render(request, "list.html", todos=pending, title="Todos")

    # ------------------------------------------------------------------
    # Add todo (must be before /todos/{todo_id} to avoid path param match)
    # ------------------------------------------------------------------

    @app.get("/todos/add")
    async def show_add_form(
        request: Request,
        user_id: str = Depends(_require_login),
        error: Optional[str] = None,
    ) -> Response:
        """Render the add todo form."""
        return _render(
            request, "add.html", title="Add Todo", error=error,
        )

    @app.post("/todos/add")
    async def add_todo(
        request: Request,
        title: str = Form(default=""),
        description: str = Form(default=""),
        due: Optional[str] = Form(default=""),
        priority: str = Form(default="medium"),
        storage: TodoStorage = Depends(_storage),
        user_id: str = Depends(_require_login),
    ) -> Response:
        """Create a new todo and redirect to the list."""
        if not title or not title.strip():
            return _render(
                request, "add.html", title="Add Todo",
                error="Title is required",
            )
        due_clean = _validate_due_date(due) if due else ""
        todo = Todo(
            title=title,
            description=description,
            due=due_clean,
            completed=False,
            created_at=datetime.now().isoformat(),
            priority=priority,
            user_id=user_id,
        )
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
            request, "edit.html", title="Edit Todo", todo=todo, error=None,
        )

    @app.post("/todos/{todo_id}/edit")
    async def edit_todo(
        request: Request,
        todo_id: str,
        title: str = Form(default=""),
        description: str = Form(default=""),
        due: Optional[str] = Form(default=""),
        priority: str = Form(default="medium"),
        storage: TodoStorage = Depends(_storage),
        user_id: str = Depends(_require_login),
    ) -> Response:
        """Update an existing todo and redirect to the list."""
        todo = storage.get(todo_id, user_id=user_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        if not title or not title.strip():
            return _render(
                request, "edit.html", title="Edit Todo", todo=todo,
                error="Title is required",
            )
        due_clean = _validate_due_date(due) if due else ""
        storage.modify(
            todo_id,
            title=title,
            description=description,
            due=due_clean,
            priority=priority,
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
        todo = storage.get(todo_id, user_id=user_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        storage.complete(todo_id)
        todo.completed = True

        if request.headers.get("HX-Request"):
            return _render(
                request, "list_row.html", todo=todo, title="Todos",
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
        todo = storage.get(todo_id, user_id=user_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        storage.delete(todo_id)

        if request.headers.get("HX-Request"):
            todos = storage.load(user_id=user_id)
            pending = [t for t in todos if not t.completed]
            return _render(
                request, "list.html", todos=pending, title="Todos",
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


def create_web_app(storage_path: Optional[str] = None) -> FastAPI:
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
