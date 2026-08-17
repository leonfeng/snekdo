## Why

The FastAPI REST API endpoints for completing, modifying, and deleting todos
perform an initial authorization check by filtering the todo lookup by the
authenticated user's ID, but the subsequent storage mutations (`complete`,
`modify`, `delete`) are called **without** the `user_id` filter. This means an
authenticated user can mutate or remove any other user's todo simply by
guessing or obtaining the target todo's ID, since the storage layer operates
on the global todo store.

## What Changes

- Fix `POST /api/v1/todos/{todo_id}/complete` to pass `user_id=current_user.id`
  to `storage.complete()`.
- Fix `PUT /api/v1/todos/{todo_id}` to pass `user_id=current_user.id` to both
  `storage.modify()` and the follow-up `storage.get()`.
- Fix `DELETE /api/v1/todos/{todo_id}` to pass `user_id=current_user.id` to
  `storage.delete()`.
- Add a spec requirement covering per-user filtering for modify/complete/delete
  operations so the bug is guarded by tests.

## Capabilities

### Modified Capabilities

- `fastapi-backend`: extend the "Per-user todo filtering" requirement to cover
  complete, modify, and delete operations, ensuring each mutates only the
  authenticated user's own todo.

## Impact

- Affected code: `snekdo/api.py` (complete_todo, modify_todo, delete_todo),
  `snekdo/storage.py` (already supports `user_id` filtering; no changes needed
  beyond the API call sites).
- No new dependencies. No breaking API changes — the behavior is a bug fix.
- Tests should verify that user A cannot modify/delete/complete user B's todo.
