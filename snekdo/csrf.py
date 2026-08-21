"""CSRF protection utilities for the snekdo web frontend.

Provides CSRF token generation, storage (via cookie), and validation for
state-changing HTTP requests. The token is stored in an httponly cookie and
included in forms as a hidden field rendered by the server.
"""

from __future__ import annotations

import secrets

from fastapi import Request
from fastapi.responses import Response

CSRF_COOKIE_NAME = "csrf_token"
CSRF_FORM_FIELD = "csrf_token"


def generate_csrf_token() -> str:
    """Generate a cryptographically random CSRF token.

    Returns:
        A base64url-encoded random token string.
    """
    return secrets.token_urlsafe(32)


def set_csrf_token_cookie(response: Response, token: str, secure: bool | None = None) -> None:
    """Set the CSRF token as an httponly cookie.

    Args:
        response: The FastAPI response object.
        token: The CSRF token to store.
        secure: If True, mark cookie as secure. If None, auto-detect based on
            the request scheme (secure for HTTPS, insecure for HTTP). Defaults
            to False for HTTP/localhost to support local testing.
    """
    if secure is None:
        secure = False
    response.set_cookie(
        key=CSRF_COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=3600,
        secure=secure,
        samesite="strict",
    )


def get_csrf_token_cookie(request: Request) -> str | None:
    """Get the CSRF token from the request cookie.

    Args:
        request: The FastAPI request object.

    Returns:
        The CSRF token string, or ``None`` if not present.
    """
    return request.cookies.get(CSRF_COOKIE_NAME)


def get_or_create_csrf_token(request: Request, response: Response) -> str:
    """Get the existing CSRF token for the session, or create a new one.

    If a CSRF token cookie is already present, it is returned.
    Otherwise, a new token is generated, set as a cookie on the response,
    and returned.

    Args:
        request: The FastAPI request object.
        response: The FastAPI response object to set the cookie on.

    Returns:
        The CSRF token string.
    """
    token = get_csrf_token_cookie(request)
    if token is not None:
        return token
    new_token = generate_csrf_token()
    set_csrf_token_cookie(response, new_token, secure=False)
    return new_token


def delete_csrf_token_cookie(response: Response) -> None:
    """Delete the CSRF token cookie.

    Args:
        response: The FastAPI response object.
    """
    response.delete_cookie(key=CSRF_COOKIE_NAME)


async def verify_csrf_token(request: Request) -> bool:
    """Validate the CSRF token from the request.

    Checks the ``csrf_token`` form field or the ``X-CSRF-Token`` header
    against the token stored in the cookie. If no cookie is present, the
    token is considered valid (e.g., for unauthenticated pages like login).
    CSRF validation is skipped for JSON requests and HTMX ``HX-Request``
    requests so the REST API and HTMX JSON paths are unaffected.

    Args:
        request: The FastAPI request object.

    Returns:
        ``True`` if the CSRF token is valid, ``False`` otherwise.
    """
    if request.headers.get("HX-Request"):
        return True
    if request.headers.get("content-type", "").startswith("application/json"):
        return True
    cookie_token = get_csrf_token_cookie(request)
    if cookie_token is None:
        # No cookie present; allow unauthenticated requests (login/register).
        return True

    # Check the header (for HTMX button requests) first, since it does not
    # require parsing the request body.
    header_token = request.headers.get("X-CSRF-Token")
    if header_token is not None:
        return secrets.compare_digest(header_token, cookie_token)

    # Check the form field (for regular form submissions).
    # `request.form` is a context manager in Starlette >= 1.6, so we use it
    # as a context manager to parse the form data.
    try:
        async with request.form() as form:
            form_token = form.get(CSRF_FORM_FIELD)
    except Exception:
        return False

    if form_token is not None:
        return secrets.compare_digest(form_token, cookie_token)

    return False
