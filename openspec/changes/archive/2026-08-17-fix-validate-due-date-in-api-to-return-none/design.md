# Design

## Approach

### 1. Fix `due` date normalization

The root cause is that `_validate_due_date` in `api.py` and `validate_due_date` in `__main__.py` return `""` (empty string) for empty/None dates, and callers propagate this empty string into the `Todo` model and storage.

**Changes:**
- `_validate_due_date(due_date)` in `api.py`: return `None` when `due_date` is `None` or empty.
- `validate_due_date(due_date)` in `__main__.py`: return `None` when `due_date` is `None` or empty.
- `TodoCreate.to_todo()` in `api.py`: use `due=self.due` instead of `due=self.due or ""`.
- `Todo.from_dict(data)` in `models.py`: convert `""` to `None` for the `due` field.
- Update callers in `api.py`, `__main__.py`, and `web.py` to use the `None` return value (simplify `if x else ""` to `if x else None` or remove the conditional entirely).

### 2. Add `completed` support to API modify endpoint

The `TodoUpdate` Pydantic model is missing the `completed` field, so `PUT /api/v1/todos/{id}` with `{"completed": true}` fails validation.

**Changes:**
- Add `completed: bool | None = None` to `TodoUpdate` in `api.py`.
- Update `modify_todo` in `api.py` to handle the `completed` field.
- Update `api_client.py` `update_todo` to accept and send a `completed` parameter.

### 3. Fix circular import in `web.py`

`web.py` imports `validate_due_date` from `__main__.py`, creating a circular import (since `__main__.py` imports `register_web_routes` from `web.py`).

**Changes:**
- Move the `_validate_due_date` helper to a new shared utility module `snekdo/due_date.py`.
- Update `api.py`, `__main__.py`, and `web.py` to import from `snekdo/due_date.py`.

### 4. Clean up storage.py

Remove the no-op user_id handling block in `storage.py` `add` method.

## Files modified

1. `snekdo/api.py` — `_validate_due_date`, `TodoCreate.to_todo`, `TodoUpdate`, `modify_todo`
2. `snekdo/__main__.py` — `validate_due_date`, `handle_add`, `handle_modify`
3. `snekdo/models.py` — `Todo.from_dict`
4. `snekdo/api_client.py` — `update_todo`
5. `snekdo/storage.py` — `add` method
6. `snekdo/web.py` — `add_todo`, `edit_todo`, circular import fix
7. `snekdo/due_date.py` — new shared utility module (created)