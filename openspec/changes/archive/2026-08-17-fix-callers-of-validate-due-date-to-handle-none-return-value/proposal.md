## Why

`validate_due_date()` in `snekdo.due_date` returns `str | None` — it returns `None` for empty or `None` input. The web edit form in `snekdo/web.py` calls `validate_due_date(due)` and unconditionally passes the result to `storage.modify()`. Because the form field defaults to `""`, every edit submission produces `None` from `validate_due_date`, which `storage.modify()` treats as "clear the due date", silently wiping the existing due date. This fix makes callers handle the `None` return value correctly so empty dates are preserved, not cleared.

## What Changes

- `snekdo/web.py` `edit_todo`: only pass `due` to `storage.modify()` when `validate_due_date` returns a non-`None` value; otherwise leave the existing due date untouched.
- `snekdo/__main__.py` `handle_modify`: use a truthy check for `args.due` so empty strings are not treated as a clear request when the user omitted the flag.
- `snekdo/api.py` `modify_todo`: use a truthy check for `update_data.due` so the API behaves consistently with the CLI.
- Add/update specs covering the new/modified behavior.

## Capabilities

### New Capabilities

- `web-edit-due-date`: The web edit-todo form must preserve an existing due date when the user submits the form without changing it.

### Modified Capabilities

- `todo-modification`: Clarify that empty-string due values clear the field (already intended behavior), and that omitting the due flag leaves it unchanged.
- `api-due-date-completed`: Clarify that `PUT /api/v1/todos/{id}` with an empty-string `due` clears the field, while omitting `due` leaves it unchanged.

## Impact

- Affected code: `snekdo/web.py`, `snekdo/__main__.py`, `snekdo/api.py`, `snekdo/due_date.py` (no change to the helper itself).
- No new dependencies.
- No API-breaking changes; only bug-fixing behavior changes.
