## Context

The snekdo web frontend uses FastAPI with Jinja2 templates and HTMX for partial page updates. Currently, there is no CSRF protection on any web form or state-changing request.

## Goals / Non-Goals

**Goals:**
- Add CSRF token generation, storage, and validation for all web forms.
- Rotate the CSRF token on login to prevent session fixation.
- Invalidate the CSRF token on logout.

**Non-Goals:**
- No changes to the REST API (only web frontend routes).
- No changes to the CLI sync behavior.

## Decisions

### 1. CSRF token storage

- **Decision**: Store the CSRF token in the user's session (using the existing FastAPI session). Generate with `secrets.token_hex(32)`.
- **Rationale**: This avoids adding a new dependency and works with the existing session middleware. The token is included in forms as a hidden input and validated on every POST/PUT/DELETE.
- **Alternative**: CSRF token in a cookie. But storing in session is simpler and consistent with the existing auth approach.

## Migration Plan

1. Add `get_csrf_token()` helper to generate and store CSRF token in session.
2. Add `verify_csrf_token()` helper to validate CSRF token from request.
3. Generate CSRF token on login and register, rotating on each login.
4. Include CSRF token in all forms via a template variable.
5. Add CSRF validation to all POST/PUT/DELETE web routes.
6. Invalidate CSRF token on logout.

## Open Questions

- None.