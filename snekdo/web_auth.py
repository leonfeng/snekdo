"""Authentication web routes for the snekdo HTMX frontend."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from snekdo.api_auth import (
    UserCreate,
    get_current_user,
)
from snekdo.models import User
from snekdo.storage import StorageError, UserStorage


def get_user_storage(storage_path: str | None = None) -> UserStorage:
    """Dependency that provides a :class:`UserStorage` instance."""
    if storage_path is None:
        return UserStorage()
    path = Path(storage_path)
    return UserStorage(storage_path=str(path.with_name("users.json")))


# Template directory relative to this package
TEMPLATES_DIR = Path(__file__).parent / "templates"


def _render(request: Request, template_name: str, **context) -> Response:
    """Render a Jinja2 template and return an HTML response."""
    template = request.app.state.template_env.get_template(template_name)
    return Response(template.render(**context), media_type="text/html")


def register_web_routes(router: APIRouter, storage_path: str | None = None) -> None:
    """Register authentication web routes with the given router.

    Args:
        router: The FastAPI router to register routes on.
        storage_path: Optional path to the storage file. If provided, the
            user storage will use this path.
    """

    def _get_user_storage() -> UserStorage:
        return get_user_storage(storage_path=storage_path)

    @router.get("/auth/register", response_class=HTMLResponse)
    async def register_page(request: Request) -> HTMLResponse:
        """Show the registration page."""
        return _render(request, "register.html", error=None)

    @router.post("/auth/register")
    async def register_submit(
        request: Request,
        username: str = Form(..., min_length=3, max_length=50),
        password: str = Form(..., min_length=8, max_length=128),
        user_storage: UserStorage = Depends(_get_user_storage),
    ) -> HTMLResponse:
        """Handle registration submission."""
        try:
            user_data = UserCreate(username=username, password=password)
            hashed_password = _hash_password(user_data.password)
            user = User(
                username=user_data.username,
                password_hash=hashed_password,
                created_at=datetime.now().isoformat(),
            )
            user_storage.add(user)
            return RedirectResponse(url="/auth/login", status_code=303)
        except StorageError as e:
            return _render(request, "register.html", error=str(e))

    @router.get("/auth/login", response_class=HTMLResponse)
    async def login_page(request: Request) -> HTMLResponse:
        """Show the login page."""
        return _render(request, "login.html", error=None)

    @router.post("/auth/login")
    async def login_submit(
        request: Request,
        username: str = Form(..., min_length=3, max_length=50),
        password: str = Form(..., min_length=8, max_length=128),
        user_storage: UserStorage = Depends(_get_user_storage),
        response: Response = None,
    ) -> HTMLResponse:
        """Handle login submission."""
        user = user_storage.get(username)
        if user is None or not _verify_password(password, user.password_hash):
            return _render(
                request, "login.html", error="Incorrect username or password"
            )

        token = _create_access_token(user.id)
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(
            key="token",
            value=token,
            httponly=True,
            max_age=3600,
        )
        return response

    @router.get("/auth/logout")
    async def logout(
        request: Request,
        response: Response = None,
    ) -> HTMLResponse:
        """Handle logout."""
        response = RedirectResponse(url="/auth/login", status_code=303)
        response.delete_cookie(key="token")
        return response

    @router.get("/auth/verify")
    async def verify_token(
        token: str | None = None,
        user: User | None = Depends(get_current_user),
    ) -> dict:
        """Verify a token and return the user info."""
        if user is None and token is None:
            return {"authenticated": False}
        return {"authenticated": True, "user_id": user.id if user else None}


# ---------------------------------------------------------------------------
# Helper functions (kept private to avoid exposing auth internals)
# ---------------------------------------------------------------------------


def _hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    from snekdo.auth import hash_password

    return hash_password(password)


def _verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against a hash."""
    from snekdo.auth import verify_password

    return verify_password(password, password_hash)


def _create_access_token(user_id: str) -> str:
    """Create a JWT access token."""
    from snekdo.auth import create_access_token

    return create_access_token(user_id)
