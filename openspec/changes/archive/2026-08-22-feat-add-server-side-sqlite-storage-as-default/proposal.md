## Why

The snekdo application currently stores todos in a JSON file at `~/.snekdo/todos.json`. Adding SQLite as the default storage backend would provide faster read/write performance, better concurrency handling, and more robust data integrity for users with large todo lists.

## What Changes

- **New Capability**: `storage/sqlite` - Introduce SQLite as the default storage backend for todos, replacing the current JSON-based storage.

## Capabilities

### New Capabilities

- `storage/sqlite`: Add SQLite-backed storage for todo persistence. This capability introduces a new storage implementation using SQLite instead of JSON files, providing improved performance and concurrency.

### Modified Capabilities

- None

## Impact

- New storage module in `snekdo/storage.py` with SQLite backend
- Updated `TodoStorage` to support SQLite as default
- Migration path from JSON to SQLite storage
- API changes: storage path format may change from JSON file path to SQLite database path
