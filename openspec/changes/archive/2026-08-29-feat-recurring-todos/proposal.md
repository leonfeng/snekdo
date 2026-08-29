## Why

Users with repeated obligations (watering plants, weekly reports, monthly bills) must re-create the same todo every cycle. Recurring todos let a user create a task once, choose a repeat interval, and have snekdo auto-recreate it as pending after completion, removing the manual re-entry overhead.

## What Changes

- **New CLI flag** `--repeat daily|weekly|monthly|yearly` (default `none`) on the `add` command.
- **New model fields** on `Todo`: `repeat` (default `none`) and `last_completed_at` (ISO 8601 or `None`).
- **New repeat logic** `next_due_date(todo, now)`: given a completed todo with a repeat rule, compute the next due date.
- **Auto-recurrence on completion**: when `TodoStorage.complete_todo()` (and the API `POST /api/v1/todos/{id}/complete`) marks a recurring todo complete, the system SHALL immediately create a new pending todo that inherits the repeat rule, title, description, priority, and `user_id`, with `due` set to the computed next occurrence. The original todo stays completed with `last_completed_at` set.
- **API changes**: `POST /api/v1/todos` and `PUT /api/v1/todos/{id}` accept an optional `repeat` field (validated against the enum); `GET` responses include `repeat` and `last_completed_at`.
- **Web form**: the add-todo form on the web frontend gets a repeat dropdown; the recurring todo's new occurrence appears in the list with the computed due date.
- **Display**: list output shows a small repeat indicator (e.g., `(weekly)`) for recurring todos.

No **BREAKING** changes: existing todos without a `repeat` field load with `repeat="none"` and are unaffected by the completion flow.

## Capabilities

### New Capabilities

- `recurring-todos`: repeat rule model fields, next-due-date computation, and auto-creation of the next occurrence upon completion.

### Modified Capabilities

- `todo-model`: `Todo` gains `repeat` and `last_completed_at` fields; `from_dict`/`to_dict` round-trip the new fields with safe defaults.
- `todo-modification`: completing a recurring todo triggers creation of a new pending occurrence (this is a requirement-level behavior change, not just implementation detail).
- `api-due-date-completed`: `POST`/`PUT` accept the `repeat` field; `TodoResponse` includes `repeat` and `last_completed_at`; completing via the API triggers recurrence.
- `e2e-todo-complete`: existing e2e completion flow must be updated to cover recurring-todo recurrence.

## Impact

- **Code**: `snekdo/models.py` (new fields + `next_due_date`), `snekdo/storage.py` (`complete_todo` recurrence hook), `snekdo/api.py` (Pydantic models, completion endpoint, recurrence trigger), `snekdo/__main__.py` (`add` flag, list display), web templates (add form + list indicator).
- **API**: new optional `repeat` field in request/response bodies; no endpoint shape changes otherwise.
- **Storage format**: JSON gains two optional keys per todo; older files load cleanly.
- **Dependencies**: none (standard library `datetime`/`dateutil`-free logic).
- **Tests**: new unit tests in `tests/` for model round-trip, `next_due_date`, recurrence on completion, API field round-trip; new/updated e2e test for the recurring flow.
