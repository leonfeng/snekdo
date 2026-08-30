# Proposal: Tags & Categories — Storage

## Why

The model can now hold `tags` and `category`, but they must survive persistence in both backends and flow through recurrence. This slice makes storage round-trip both fields on JSON and SQLite.

## What Changes

- `TodoStorage.modify()` (JSON path) accepts `tags` and `category` kwargs.
- SQLite schema gains `tags` (TEXT, JSON-encoded list) and `category` (TEXT) columns, with an in-place `ALTER TABLE` migration (column-exists guard) for existing databases.
- All `TodoStorageSQLite` CRUD paths read and write the new fields.
- Recurrence in both backends copies `tags` and `category` to the next occurrence.

## Capabilities

### New Capabilities

(none — this slice implements persistence for the `todo-tags` capability defined in the model slice)

### Modified Capabilities

- `todo-tags`: storage persistence, serialization in SQLite, migration, and recurrence behavior for `tags` and `category`.

## Impact

- `snekdo/storage.py`: `modify()` kwargs (JSON path).
- `snekdo/storage_sqlite.py`: schema init + migration, all CRUD paths, recurrence.
- Tests: storage tests for JSON and SQLite persistence, modify, migration on a pre-existing DB, and recurrence copying tags/category.
