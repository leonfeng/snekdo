## 1. Wire `--storage` flag to all handlers

- [x] 1.1 In `handle_add`, change `TodoStorage()` to `TodoStorage(storage_path=args.storage)`
- [x] 1.2 In `handle_list`, change `TodoStorage()` to `TodoStorage(storage_path=args.storage)`
- [x] 1.3 In `handle_complete`, change `TodoStorage()` to `TodoStorage(storage_path=args.storage)`
- [x] 1.4 In `handle_delete`, change `TodoStorage()` to `TodoStorage(storage_path=args.storage)`
- [x] 1.5 In `handle_modify`, change `TodoStorage()` to `TodoStorage(storage_path=args.storage)`

## 2. Fix `handle_complete` data-loss bug

- [x] 2.1 Replace `todo.completed = True; storage.save([todo])` with `storage.complete(args.todo_id)`
- [x] 2.2 Keep the `todo = storage.get(args.todo_id)` lookup for the confirmation message
- [x] 2.3 Keep the not-found error check

## 3. Add real-storage tests

- [x] 3.1 Add test: completing a todo via real storage preserves other todos
- [x] 3.2 Add test: `--storage` flag saves to the specified path
- [x] 3.3 Add test: default path is used when `--storage` is omitted
- [x] 3.4 Add test: sorting works correctly with real storage
- [x] 3.5 Add test: `--storage` flag works for list command with real storage
- [x] 3.6 Add test: deleting a todo preserves other todos with real storage

## 4. Update existing mock tests if needed

- [x] 4.1 Verify existing `test_complete_todo` and `test_add_todo` still pass with the new `storage_path` argument
- [x] 4.2 Update mock args to include `args.storage = None` or a string if needed

## 5. Run tests and verify

- [x] 5.1 Run `pytest` and confirm all tests pass (53 tests pass)
- [x] 5.2 Run `pytest` with real-storage tests to verify the fixes
- [x] 5.3 Run linter if available (no linter configured in project)

## 6. Sync main specs

- [x] 6.1 Sync `todo-sorting` spec from archived `feat-sort-todo-list` change to `openspec/specs/todo-sorting/spec.md`
- [x] 6.2 Validate main specs with `openspec validate --specs`
