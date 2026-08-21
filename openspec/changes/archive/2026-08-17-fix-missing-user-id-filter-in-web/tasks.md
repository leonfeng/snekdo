## 1. Update Todo serialization

- [x] 1.1 Modify `Todo.to_dict()` in `snekdo/models.py` to always include the `user_id` key (even when `None`)
- [x] 1.2 Verify `Todo.from_dict()` handles both present and absent `user_id` keys (already handles `None` via `data.get`)

## 2. Update CLI add command

- [x] 2.1 Modify `handle_add()` in `snekdo/__main__.py` to set `user_id` on created todos (keep `None` for unauthenticated CLI use but ensure field is present)

## 3. Update web list filtering

- [x] 3.1 Verify web list endpoints (`index`, `list_todos`) in `snekdo/web.py` filter by authenticated user's `user_id` (already done via `storage.load(user_id=user_id)`)
- [x] 3.2 Verify web add endpoint sets `user_id` on created todos (already done)

## 4. Add/update tests

- [x] 4.1 Add test verifying `Todo.to_dict()` includes `user_id` for both owned and unowned todos
- [x] 4.2 Add test verifying CLI-created todos are visible in web list when user matches
- [x] 4.3 Add test verifying web-created todos are visible in CLI list
- [x] 4.4 Add test verifying per-user isolation in web list

## 5. Verify and run tests

- [x] 5.1 Run `pytest tests/test_models.py tests/test_web.py tests/test_cli.py` to verify changes
- [x] 5.2 Run `openspec validate "fix-missing-user-id-filter-in-web"` to validate the change