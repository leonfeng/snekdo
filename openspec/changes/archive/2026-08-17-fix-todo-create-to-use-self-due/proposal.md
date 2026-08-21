## Why

The `TodoCreate.to_todo()` method constructs a `Todo` from the raw request
data without validating the `due` field.  The API `add_todo` endpoint must
therefore validate the due date *after* building the `Todo` and then
overriding `todo.due` — a redundant two-step that is easy to forget and
leaves the intermediate `Todo` object in an invalid state.  This change
moves due-date validation into `TodoCreate.to_todo()` so that every created
`Todo` is self-validating.

## What Changes

- Add due-date validation inside `TodoCreate.to_todo()` so the created
  `Todo` always holds a valid (or `None`) due date.
- Simplify the API `add_todo` endpoint to remove the redundant validation
  and `todo.due` override.
- Simplify the web `add_todo` route to remove the redundant validation.
- Keep CLI `handle_add` validation as-is (it does not use `TodoCreate`).
- Add a delta spec to the `api-due-date-completed` capability.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `api-due-date-completed`: Add a requirement that `TodoCreate.to_todo()`
  validates the due date, ensuring created `Todo` objects never store an
  invalid due string.

## Impact

- Affected code: `snekdo/api.py` (`TodoCreate.to_todo`, `add_todo`),
  `snekdo/web.py` (`add_todo` route).
- Affected tests: `tests/test_api.py` (add tests verifying the `Todo`
  produced by `to_todo()` is validated; update existing tests as needed).
- No new dependencies.
- No breaking changes to existing valid usage.
