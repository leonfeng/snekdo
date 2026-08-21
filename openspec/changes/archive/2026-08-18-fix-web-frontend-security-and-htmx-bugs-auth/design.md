## Context

The snekdo web frontend uses FastAPI with Jinja2 templates and HTMX. The authentication web pages (login, register) currently use FastAPI Form constraints that return JSON 422 errors, and the logout route uses GET which is cacheable and CSRF-able.

## Goals / Non-Goals

**Goals:**
- Replace FastAPI Form constraints in login/register with manual validation so failures re-render the form with HTML errors.
- Change logout from GET to POST so it is not cacheable or CSRF-able.
- Update templates to use POST form for logout.

**Non-Goals:**
- No changes to the REST API authentication endpoints.
- No changes to the CLI sync behavior.
- CSRF token generation is handled by the `web-csrf` child change.
- Delete-account HTMX handling is handled by the `htmx-jinja2-frontend` child change.

## Decisions

### 1. Form validation

- **Decision**: Use manual `ValueError` raising for web form validation (matching the existing `TodoCreate.to_todo()` pattern) instead of FastAPI `Form(..., min_length=...)` constraints.
- **Rationale**: FastAPI Form constraints return JSON 422 errors; manual `ValueError` with custom messages lets us re-render the form with HTML errors.
- **Alternative**: Use `Field(..., min_length=...)` with `ValidationException`. But this still returns JSON.

### 2. Logout method

- **Decision**: Change `@router.get("/auth/logout")` to `@router.post("/auth/logout")`.
- **Rationale**: GET requests are cacheable and CSRF-able. POST is not cacheable and requires a form.
- **Alternative**: Use a different path. But keeping `/auth/logout` and changing the method is the minimal change.

## Migration Plan

1. Fix login validation to use manual validation (task 3.1).
2. Change logout to POST (task 4.1).
3. Update templates to use POST form for logout (task 4.2).

## Open Questions

- None.