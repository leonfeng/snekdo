## 1. Storage layer: add combined delete method

- [x] 1.1 Add `UserStorage.delete_user_with_todos(user_id, todo_storage)` method to `snekdo/storage.py` that removes all todos for the user and then removes the user record, returning True on success and False if the user does not exist.
- [x] 1.2 Ensure the method preserves other users' todos when deleting a user.

## 2. API layer: use combined delete method

- [x] 2.1 Update `snekdo/api.py` `delete_user_account` to call `user_storage.delete_user_with_todos(current_user.id, todo_storage)` instead of the two separate calls.
- [x] 2.2 Update `snekdo/web.py` `delete_account` to call `user_storage.delete_user_with_todos(user_id, storage)` instead of the two separate calls.

## 3. Tests

- [x] 3.1 Add tests in `tests/test_storage.py` for `UserStorage.delete_user_with_todos`: success case, other users' todos preserved, non-existent user returns False.
- [x] 3.2 Add or update tests in `tests/test_api.py` and `tests/e2e/test_account_deletion.py` to verify cascading deletion through the API.

## 4. Verification

- [x] 4.1 Run the full test suite with `uv run pytest` to verify no regressions.