## 1. Backend: Filter Helper

- [x] 1.1 Add `_filter_todos(todos, q=None, status="pending", priority=None)` helper function to `snekdo/web.py` — filters by case-insensitive title/description search, status (pending/completed/all), and priority (high/medium/low)
- [x] 1.2 Update `index()` route in `snekdo/web.py` to accept `q`, `status`, and `priority` query parameters and pass them to `_filter_todos`
- [x] 1.3 Update `list_todos()` route in `snekdo/web.py` to accept `q`, `status`, and `priority` query parameters and pass them to `_filter_todos`
- [x] 1.4 Pass `q`, `status`, and `priority` values in the template context for both `index` and `list_todos` routes

## 2. Frontend: Filter Bar Template

- [x] 2.1 Add filter bar markup to `snekdo/templates/list.html`: a search `<input>` with `hx-get="/todos"` and `hx-trigger="keyup changed delay:300ms"`, a `<select>` for status (all/pending/completed) with `hx-trigger="change"`, and a `<select>` for priority (all/high/medium/low) with `hx-trigger="change"` — all targeting `#todo-table-wrapper`
- [x] 2.2 Pre-fill filter bar inputs with current `q`, `status`, and `priority` values from the template context
- [x] 2.3 Wrap the existing `<table>` and empty-state `<p>` in a `<div id="todo-table-wrapper">` for HTMX partial swaps
- [x] 2.4 Make the completed-todos `<details>` section conditional — only render when `status != "pending"` and at least one completed todo exists in the filtered set

## 3. Testing

- [x] 3.1 Add unit/integration tests in `tests/` verifying `_filter_todos` behavior: search by title, search by description, case-insensitivity, status filtering (pending/completed/all), priority filtering, combined filters (AND semantics), and default behavior (no params = pending only)
- [x] 3.2 Add web route tests verifying that `GET /todos?q=...`, `GET /todos?status=...`, and `GET /todos?priority=...` return 200 and render the correct filtered content
- [x] 3.3 Add a web route test verifying that filter values are reflected in the rendered HTML (pre-filled input values and selected options)
- [x] 3.4 Run the full test suite (`uv run pytest`) and confirm all tests pass
