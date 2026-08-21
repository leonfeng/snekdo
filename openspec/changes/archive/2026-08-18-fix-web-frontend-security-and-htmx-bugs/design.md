## Context

The snekdo web frontend uses FastAPI with Jinja2 templates and HTMX for partial page updates. The current implementation has no CSRF protection, several HTMX rendering bugs, and inconsistent error handling between JSON API responses and HTML form responses.

## Goals / Non-Goals

**Goals:**
- Add CSRF token generation, storage, and validation for all web forms.
- Fix HTMX rendering bugs (delete empty state, profile form targets, complete stale object).
- Make all web forms return HTML errors instead of JSON 422 responses.
- Change logout from GET to POST.
- Make delete-account handle HTMX requests properly.
- Add validation for priority field and due-date empty-string handling.
- Add e2e tests for the new behavior.

**Non-Goals:**
- No changes to the REST API (only web frontend routes).
- No changes to the CLI sync behavior.
- No changes to the storage backend or todo model.

## Decisions

### 1. CSRF token storage
- **Decision**: Store the CSRF token in the user's session (using the existing `fastapi-session` or a simple session dict). Generate with `secrets.token_hex(32)`.
- **Rationale**: This avoids adding a new dependency and works with the existing session middleware. The token is included in forms as a hidden input and validated on every POST/PUT/DELETE.
- **Alternative**: CSRF token in a cookie. But storing in session is simpler and consistent with the existing auth approach.

### 2. Form validation
- **Decision**: Use manual `ValueError` raising for web form validation (matching the existing `TodoCreate.to_todo()` pattern) instead of FastAPI `Form(..., min_length=...)` constraints.
- **Rationale**: FastAPI Form constraints return JSON 422 errors; manual `ValueError` with custom messages lets us re-render the form with HTML errors.
- **Alternative**: Use `Field(..., min_length=...)` with `ValidationException`. But this still returns JSON.

### 3. Logout method
- **Decision**: Change `@router.get("/auth/logout")` to `@router.post("/auth/logout")`.
- **Rationale**: GET requests are cacheable and CSRF-able. POST is not cacheable and requires a form.
- **Alternative**: Use a different path. But keeping `/auth/logout` and changing the method is the minimal change.

### 4. Delete HTMX empty state
- **Decision**: Render the empty state as a `<p class="empty">` inside the `<tbody>` using `hx-target="tbody#todo-list"` instead of `hx-target="tr#todo-{id}"` with `hx-swap="outerHTML"`.
- **Rationale**: Swapping `outerHTML` of a `<tr>` with a `<p>` produces invalid HTML. Targeting the `<tbody>` and swapping `innerHTML` (or `outerHTML` of the tbody) is valid.
- **Alternative**: Keep the `<tr>` target but render an empty `<tr>` with a colspan. But this still shows a row border.

### 5. Complete todo stale object
- **Decision**: Load the todo fresh from storage inside `complete_todo` before calling `storage.complete()`.
- **Rationale**: The current code loads the todo, calls `storage.complete()` (which loads a new instance), then sets `todo.completed = True` on the old instance. This is redundant and confusing.
- **Alternative**: Remove the stale assignment entirely.

### 6. Delete account HTMX
- **Decision**: Check `request.headers.get("HX-Request")` and return HTML (redirect or message) instead of always redirecting.
- **Rationale**: HTMX requests expect HTML content back, not a 302 redirect.
- **Alternative**: Always redirect and let HTMX follow. But HTMX doesn't follow 302 redirects by default for POST/DELETE.

## Risks / Trade-offs

- **Risk**: Session-based CSRF tokens require session storage. If sessions are not properly initialized, the token may be missing.
  - **Mitigation**: Ensure session middleware is configured before CSRF checks.
- **Risk**: Existing e2e tests may fail because logout is now POST and CSRF tokens are required.
  - **Mitigation**: Update e2e tests to include CSRF tokens and use POST for logout.
- **Risk**: The `secrets.token_hex` approach may not be compatible with all FastAPI session configurations.
  - **Mitigation**: Use the existing session object from FastAPI.

## Migration Plan

1. Add CSRF token generation to the session (in login/register).
2. Add a `get_csrf_token()` helper and a `verify_csrf_token()` function.
3. Include CSRF token in all forms via a template variable.
4. Add CSRF validation to state-changing routes.
5. Fix the delete HTMX target and swap.
6. Fix the complete todo handler.
7. Fix login validation to use manual validation.
8. Change logout to POST.
9. Fix delete account HTMX handling.
10. Fix add/edit todo validation to catch Pydantic v2 errors.
11. Add priority field validation.
12. Fix due-date empty string handling.
13. Update e2e tests.
14. Run tests and verify.

## Open Questions

- Should the CSRF token be stored in the session or in a cookie? → Session (simpler, consistent with existing auth).
- Should the delete account HTMX request return a redirect or a message? → Return a message that updates the page.