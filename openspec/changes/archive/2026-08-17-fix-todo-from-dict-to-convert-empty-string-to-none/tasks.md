## 1. Update `Todo.from_dict()` in `snekdo/models.py`

- [x] 1.1 Change `user_id=data.get("user_id")` to `user_id=data.get("user_id") or None` so empty strings are normalized to `None`.
- [x] 1.2 Verify `due=data.get("due") or None` is already present (no change needed).

## 2. Update tests in `tests/test_models.py`

- [x] 2.1 Add a test verifying `Todo.from_dict()` converts empty string `due` to `None`.
- [x] 2.2 Add a test verifying `Todo.from_dict()` converts empty string `user_id` to `None`.
- [x] 2.3 Update `test_todo_from_dict_without_user_id` to also verify empty string `user_id` becomes `None`.

## 3. Validate the change

- [x] 3.1 Run `uv run pytest tests/test_models.py` to verify the model tests pass.
- [x] 3.2 Run `uv run pytest` to ensure no regressions in the full test suite.
