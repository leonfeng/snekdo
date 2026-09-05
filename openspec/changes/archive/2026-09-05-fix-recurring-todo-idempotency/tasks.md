## 1. Core Implementation

- [x] 1.1 Add `and not todo.completed` guard to the JSON `TodoStorage.complete()` path in `snekdo/storage.py` so completing an already-completed recurring todo does not spawn a duplicate occurrence (mirrors `storage_sqlite.py:283`).

## 2. Tests

- [x] 2.1 Add a JSON-backend regression test in `tests/test_storage.py` verifying that completing the same recurring todo twice creates only one pending occurrence.
- [x] 2.2 Add a SQLite-backend regression test in `tests/test_storage.py` verifying the same idempotency invariant holds on the SQLite path.
