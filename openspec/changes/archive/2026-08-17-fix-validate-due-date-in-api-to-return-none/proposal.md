# Proposal: Fix due-date validation and completed-status update

## What

This change fixes two related bugs in the snekdo codebase:

1. **Due dates are stored as empty strings (`""`) instead of `None`** when a todo is created or updated without a due date. This affects the API (`api.py`), CLI (`__main__.py`), and web frontend (`web.py`).

2. **The API cannot update the `completed` status of a todo via `PUT /api/v1/todos/{id}`** because the `TodoUpdate` Pydantic model is missing the `completed` field. This means the API's modify endpoint silently ignores `completed` updates and returns `422 No fields to update`.

## Why

- Storing `due` as `""` instead of `None` causes inconsistent data: `Todo.from_dict` returns an empty string for `due` when it should be `None`, and the JSON file stores `""` instead of `null`.
- The `TodoUpdate` model missing `completed` means users cannot mark todos as complete through the API (the primary programmatic interface), breaking the expected CRUD contract.
- The web frontend's `_validate_due_date` function imports from `__main__.py`, creating a circular import dependency.

## Scope

- `snekdo/api.py`: `_validate_due_date` returns `None` for empty dates; `TodoUpdate` gains a `completed` field; `modify_todo` handles `completed`.
- `snekdo/__main__.py`: `validate_due_date` returns `None` for empty dates; callers simplified.
- `snekdo/models.py`: `Todo.from_dict` converts `""` to `None` for `due`.
- `snekdo/api_client.py`: `update_todo` gains a `completed` parameter.
- `snekdo/storage.py`: Remove no-op user_id handling block.
- `snekdo/web.py`: Move `_validate_due_date` to a shared utility to avoid circular import.

## Out of scope

- Changes to the JWT token generation or authentication flow (login already returns `access_token`).
- Changes to the sync protocol or storage file format beyond the `due` value normalization.