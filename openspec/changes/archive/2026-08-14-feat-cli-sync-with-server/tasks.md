## 1. HTTP Client Module

- [x] 1.1 Create `snekdo/api_client.py` with a `ServerHttpClient` class
- [x] 1.2 Implement `get_todos` method to fetch all todos from the server
- [x] 1.3 Implement `get_todo` method to fetch a single todo by ID
- [x] 1.4 Implement `create_todo` method to create a new todo on the server
- [x] 1.5 Implement `update_todo` method to update an existing todo on the server
- [x] 1.6 Implement `delete_todo` method to delete a todo on the server
- [x] 1.7 Implement `complete_todo` method to mark a todo as complete on the server
- [x] 1.8 Handle connection errors and invalid URLs gracefully

## 2. Sync Command Implementation

- [x] 2.1 Add `sync` subcommand to the CLI parser in `snekdo/__main__.py`
- [x] 2.2 Add `--server` flag (default `http://127.0.0.1:8000`)
- [x] 2.3 Add `--direction` flag with choices `pull`, `push`, `both` (default `both`)
- [x] 2.4 Add `--storage` flag for local storage path
- [x] 2.5 Implement `handle_sync` function with pull logic
- [x] 2.6 Implement `handle_sync` function with push logic
- [x] 2.7 Implement `handle_sync` function with both logic
- [x] 2.8 Implement conflict resolution (server wins on pull/both, local wins on push)
- [x] 2.9 Print sync summary (count of pulled, pushed, updated, deleted todos)

## 3. Tests

- [x] 3.1 Add tests for `ServerHttpClient` in `tests/test_api.py`
- [x] 3.2 Add tests for the `sync` command in `tests/test_cli.py`
- [x] 3.3 Add tests for conflict resolution
- [x] 3.4 Add tests for server-unavailable handling

## 4. Validation

- [x] 4.1 Run `openspec validate` to verify the change
- [x] 4.2 Run `pytest` to verify all tests pass
