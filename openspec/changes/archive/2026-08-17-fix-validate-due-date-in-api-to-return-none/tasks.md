# Tasks

- [x] 1. Create `snekdo/due_date.py` with shared `_validate_due_date` function
- [x] 2. Update `snekdo/api.py`: `_validate_due_date` returns `None` for empty dates, `TodoCreate.to_todo()` uses `due=self.due`, `TodoUpdate` adds `completed` field, `modify_todo` handles `completed`
- [x] 3. Update `snekdo/__main__.py`: `validate_due_date` returns `None` for empty dates, simplify callers in `handle_add` and `handle_modify`
- [x] 4. Update `snekdo/models.py`: `Todo.from_dict` converts `""` to `None` for `due`
- [x] 5. Update `snekdo/api_client.py`: `update_todo` accepts and sends `completed` parameter
- [x] 6. Update `snekdo/storage.py`: remove no-op user_id handling block in `add`, add `completed` handling in `modify`
- [x] 7. Update `snekdo/web.py`: import from `snekdo/due_date.py`, fix `add_todo` and `edit_todo` due date handling
- [x] 8. Update delta spec: `specs/api-due-date-completed/spec.md`
- [x] 9. Run tests to verify all fixes (241 non-e2e tests pass)