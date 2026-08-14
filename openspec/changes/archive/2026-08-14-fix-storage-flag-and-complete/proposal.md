## Why

Two critical bugs exist in the CLI layer that cause data loss and broken functionality:

1. The `--storage` flag is parsed by argparse but never used — every handler creates `TodoStorage()` with the default path `~/.snekdo/todos.json`, so the user's custom storage path is silently ignored.
2. The `complete` command manually sets `todo.completed = True` and then calls `storage.save([todo])`, which overwrites the entire JSON file with only the completed todo, **permanently deleting all other todos**.

Both bugs are not caught by the existing test suite because the handlers are tested with mocked `TodoStorage`.

## What Changes

- Wire the `--storage` argument through to every `TodoStorage()` instantiation.
- Replace the manual `storage.save([todo])` in `handle_complete` with `storage.complete(args.todo_id)`, which correctly updates all todos.
- Add tests that exercise the real storage behavior (not mocked) for these two scenarios.

## Capabilities

### Modified Capabilities

- `todo-sorting` / `todo-modification` / `todo-priority`: No new capability, but the underlying storage and CLI layer are corrected.

## Impact

- **Code**: `snekdo/__main__.py` (all handlers), `snekdo/storage.py` (no changes needed — its API is already correct).
- **Tests**: New tests in `tests/test_cli.py` covering real-storage complete and storage-flag behavior.
- **CLI**: `--storage` begins working as documented; `complete` no longer loses data.
- **Backward compatibility**: Default behavior preserved when `--storage` is omitted.
