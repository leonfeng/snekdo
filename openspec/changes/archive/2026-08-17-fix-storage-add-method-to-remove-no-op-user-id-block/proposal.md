## Why

`UserStorage.delete_user(user_id)` removes the user record but leaves the user's todos in the todo storage file. The cascading deletion of a user's todos is currently performed by the API and web layers calling `TodoStorage.delete_all_user_todos(user_id)` before `UserStorage.delete_user(user_id)`. This scatters the account-deletion contract across multiple classes and is easy to forget. The `delete_user` method is effectively a no-op with respect to the user's todo data — it accepts a `user_id` but does not remove that user's todos.

## What Changes

- Add a `delete_user_with_todos(user_id, todo_storage)` method to `UserStorage` that removes all todos belonging to the user and then removes the user record, in a single atomic operation.
- Update the API (`delete_user_account`) and web (`delete_account`) account-deletion handlers to use the new method instead of calling the two storage methods separately.
- Add tests covering the new storage method and the cascading deletion behavior.

## Capabilities

### New Capabilities

- `storage-user-deletion`: Covers the `UserStorage.delete_user_with_todos` method and its cascading deletion behavior.

### Modified Capabilities

- `user-account-deletion`: Adds a requirement for the combined `delete_user_with_todos` storage method and updates the cascading deletion scenarios.

## Impact

- Affected code: `snekdo/storage.py`, `snekdo/api.py`, `snekdo/web.py`, `tests/test_storage.py`, `tests/test_api.py`, `tests/e2e/test_account_deletion.py`
- No new dependencies.
- No breaking API changes.