## Context

The snekdo web frontend uses FastAPI with Jinja2 templates and HTMX for partial page updates. The current implementation has several HTMX rendering bugs and inconsistent error handling between JSON API responses and HTML form responses.

## Goals / Non-Goals

**Goals:**
- Fix HTMX rendering bugs (delete empty state, profile form targets, complete stale object).
- Make all web forms return HTML errors instead of JSON 422 responses.
- Add validation for priority field and due-date empty-string handling.

**Non-Goals:**
- No changes to the REST API (only web frontend routes).
- No changes to the CLI sync behavior.
- CSRF token generation is handled by the `web-csrf` child change.

## Decisions

### 1. Form validation

- **Decision**: Use manual `ValueError` raising for web form validation (matching the existing `TodoCreate.to_todo()` pattern) instead of FastAPI `Form(..., min_length=...)` constraints.
- **Rationale**: FastAPI Form constraints return JSON 422 errors; manual `ValueError` with custom messages lets us re-render the form with HTML errors.
- **Alternative**: Use `Field(..., min_length=...)` with `ValidationException`. But this still returns JSON.

### 2. Delete HTMX empty state

- **Decision**: Render the empty state as a `<p class="empty">` inside the `<tbody>` using `hx-target="tbody#todo-list"` instead of `hx-target="tr#todo-{id}"` with `hx-swap="outerHTML"`.
- **Rationale**: Swapping `outerHTML` of a `<tr>` with a `<p>` produces invalid HTML. Targeting the `<tbody>` and swapping `innerHTML` (or `outerHTML` of the tbody) is valid.
- **Alternative**: Keep the `<tr>` target but render an empty `<tr>` with a colspan. But this still shows a row border.

### 3. Complete todo stale object

- **Decision**: Load the todo fresh from storage inside `complete_todo` before calling `storage.complete()`.
- **Rationale**: The current code loads the todo, calls `storage.complete()` (which loads a new instance), then sets `todo.completed = True` on the old instance. This is redundant and confusing.
- **Alternative**: Remove the stale assignment entirely.

### 4. Delete account HTMX

- **Decision**: Check `request.headers.get("HX-Request")` and return HTML (redirect or message) instead of always redirecting.
- **Rationale**: HTMX requests expect HTML content back, not a 302 redirect.
- **Alternative**: Always redirect and let HTMX follow. But HTMX doesn't follow 302 redirects by default for POST/DELETE.

## Migration Plan

1. Fix the delete HTMX target and swap (task 2.1).
2. Fix the profile form HTMX target (task 2.2).
3. Fix the complete todo handler to load fresh instance (task 2.3).
4. Fix the delete account HTMX handling (task 2.4).
5. Fix add/edit todo validation to catch Pydantic v2 errors (task 3.2).
6. Add priority field validation (task 3.3).
7. Fix due-date empty string handling (task 3.4).

## Open Questions

- None.