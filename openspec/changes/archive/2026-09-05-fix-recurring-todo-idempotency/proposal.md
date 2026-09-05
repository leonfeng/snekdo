## Why

The recurring-todos spec requires that completing an already-completed occurrence be a no-op for recurrence (idempotent), but the JSON storage path in `storage.py:complete()` spawns a duplicate pending occurrence every time `complete()` is called — even on an already-completed todo. Double-completing a recurring todo (e.g. via CLI then API, or a retry) creates duplicate occurrences, breaking the invariant.

## What Changes

- Add a `not todo.completed` guard to the JSON storage `complete()` path so that completing an already-completed recurring todo does not create a new occurrence (matches the SQLite backend, which already has this guard).
- Add a regression test covering double-completion of a recurring todo across both JSON and SQLite backends.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `recurring-todos`: Strengthen/verify the idempotency requirement so it is enforced by both storage backends, not just SQLite.

## Impact

- `snekdo/storage.py` — JSON `TodoStorage.complete()` gains an idempotency guard.
- `snekdo/storage_sqlite.py` — no change (already correct); used as the reference behavior.
- `tests/test_storage.py` — new regression tests for double-completion idempotency.
- No API/CLI surface changes; behavior is a bug fix.
