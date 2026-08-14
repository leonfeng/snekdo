## Context

`snekdo/__main__.py` defines a global `--storage` argument (line 23) but none of the five command handlers (`handle_add`, `handle_list`, `handle_complete`, `handle_delete`, `handle_modify`) pass it to `TodoStorage()`. Every handler calls `TodoStorage()` with no arguments, forcing the default `~/.snekdo/todos.json` path.

Additionally, `handle_complete` (lines 155-163) does:
```python
todo = storage.get(args.todo_id)
todo.completed = True
storage.save([todo])  # saves ONLY this one todo
```
This is wrong because `storage.save()` replaces the entire file contents with the provided list. The correct approach is to use `storage.complete(args.todo_id)`, which loads all todos, flips the matching one's `completed` flag, and saves the full list.

## Goals / Non-Goals

**Goals:**
- Every handler creates `TodoStorage(storage_path=args.storage)` so the `--storage` flag is respected.
- `handle_complete` uses `storage.complete(args.todo_id)` instead of manually saving a single todo.
- Add tests that use a real temporary storage file (not mocked `TodoStorage`) to verify both fixes.

**Non-Goals:**
- No changes to `storage.py` (its API is already correct).
- No refactoring of the handler signature pattern.
- No new CLI features.

## Decisions

### Decision: Pass `args.storage` to `TodoStorage()` in every handler

**Choice**: Change each `storage = TodoStorage()` to `storage = TodoStorage(storage_path=args.storage)`.

**Rationale**: `TodoStorage.__init__` already handles `None` by falling back to the default path, so this is safe whether `--storage` is provided or not. Minimal change, no new abstractions.

### Decision: Use `storage.complete(args.todo_id)` in `handle_complete`

**Choice**: Replace the manual `todo.completed = True; storage.save([todo])` with `storage.complete(args.todo_id)`.

**Rationale**: `storage.complete()` already implements the correct behavior: load all todos, find the matching one, set `completed=True`, save the full list. Reusing it eliminates the data-loss bug and reduces code.

### Decision: Add real-storage tests

**Choice**: Add two new tests in `tests/test_cli.py` that create a real temporary JSON file, call the CLI handler directly, and verify the file contents afterward.

**Rationale**: Mocked tests cannot catch these bugs because they never touch the file system. Real-storage tests are the only way to verify the fix.

## Risks / Trade-offs

### Risk: Existing tests rely on mocked `TodoStorage`

**Impact**: The existing `test_complete_todo` and `test_add_todo` tests mock `TodoStorage`. They will continue to pass because the handlers still call `TodoStorage()`, just with an extra argument. However, the mock's `storage_path` argument will be `None` (since the test passes `args.storage` as a mock attribute, not a real path).

**Mitigation**: The tests use `patch('snekdo.__main__.TodoStorage')` which returns a `MagicMock`. Passing `storage_path=args.storage` to a `MagicMock` constructor is harmless. The existing tests should continue to pass.

### Risk: `args.storage` might not be set in some test mocks

**Impact**: Some test mocks set `args.storage = str(storage_file)` but others might not. If `args.storage` is a `MagicMock` (not a string), `TodoStorage(storage_path=<MagicMock>)` might fail.

**Mitigation**: Update any test mocks to set `args.storage` to a string or `None`. The new real-storage tests will set it explicitly.

## Migration Plan

This is a pure bug fix with no migration required. Existing behavior is preserved when `--storage` is omitted.

## Open Questions

None — all requirements are clearly defined.
