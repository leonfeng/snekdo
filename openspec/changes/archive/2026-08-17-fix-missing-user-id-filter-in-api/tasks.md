## 1. Fix API mutation endpoints to scope by user_id

- [x] 1.1 In `snekdo/api.py`, pass `user_id=current_user.id` to
      `storage.complete()` in `complete_todo`.
- [x] 1.2 In `snekdo/api.py`, pass `user_id=current_user.id` to
      `storage.modify()` in `modify_todo`.
- [x] 1.3 In `snekdo/api.py`, pass `user_id=current_user.id` to the
      follow-up `storage.get()` in `modify_todo`.
- [x] 1.4 In `snekdo/api.py`, pass `user_id=current_user.id` to
      `storage.delete()` in `delete_todo`.

## 2. Add tests for cross-user mutation prevention

- [x] 2.1 Add `test_complete_cross_user_returns_404` to
      `tests/test_api.py`: create user A's todo, login as user B, attempt to
      complete user A's todo, expect 404.
- [x] 2.2 Add `test_modify_cross_user_returns_404` to `tests/test_api.py`:
      create user A's todo, login as user B, attempt to modify user A's todo,
      expect 404.
- [x] 2.3 Add `test_delete_cross_user_returns_404` to `tests/test_api.py`:
      create user A's todo, login as user B, attempt to delete user A's todo,
      expect 404.

## 3. Update spec

- [x] 3.1 Delta spec already created at
      `openspec/changes/fix-missing-user-id-filter-in-api/specs/fastapi-backend/spec.md`
      with MODIFIED "Per-user todo filtering" requirement.

## 4. Verify

- [x] 4.1 Run `uv run pytest tests/test_api.py` to confirm existing tests pass
      and new cross-user tests pass.
- [x] 4.2 Run `openspec validate --change fix-missing-user-id-filter-in-api`
      to confirm the change is valid.
