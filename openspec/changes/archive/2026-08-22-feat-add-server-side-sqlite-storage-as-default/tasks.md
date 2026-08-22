## 1. Setup SQLite storage module

- [x] 1.1 Create new `snekdo/storage_sqlite.py` module with SQLite backend
- [x] 1.2 Add SQLite database configuration and path handling

## 2. Implement core SQLite storage operations

- [x] 2.1 Implement `TodoStorageSQLite` class with CRUD operations
- [x] 2.2 Add `load()` method to read todos from SQLite database
- [x] 2.3 Add `save()` method to persist todos to SQLite database
- [x] 2.4 Implement `add()` method for new todo items
- [x] 2.5 Implement `get()` method to find todo by ID
- [x] 2.6 Implement `delete()` method to remove todo by ID
- [x] 2.7 Implement `complete()` method to mark todo as complete
- [x] 2.8 Implement `modify()` method to update todo fields

## 3. Update TodoStorage to support SQLite backend

- [x] 3.1 Add SQLite storage option to `TodoStorage` class
- [x] 3.2 Update constructor to accept storage type parameter
- [x] 3.3 Add factory method to create appropriate storage backend

## 4. Migration from JSON to SQLite

- [x] 4.1 Create migration script to convert existing JSON todos to SQLite
- [x] 4.2 Add command-line option for migration
- [x] 4.3 Test migration preserves all todo data

## 5. Update API and CLI integration

- [x] 5.1 Update `create_app()` in `snekdo/api.py` to use SQLite by default
- [x] 5.2 Update CLI subcommands to support `--storage` option for SQLite
- [x] 5.3 Ensure existing JSON storage path still works as fallback

## 6. Testing

- [x] 6.1 Write unit tests for SQLite storage operations
- [x] 6.2 Test migration from JSON to SQLite
- [x] 6.3 Test concurrent access with SQLite
- [x] 6.4 Verify existing JSON storage continues to work

## 7. Documentation

- [x] 7.1 Update module docstrings with SQLite information
- [x] 7.2 Add usage examples for SQLite storage backend
