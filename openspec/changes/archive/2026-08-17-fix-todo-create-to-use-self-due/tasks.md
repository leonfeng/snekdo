## 1. Update TodoCreate.to_todo() to validate due date

- [x] 1.1 Import `validate_due_date` from `snekdo.due_date` in `snekdo/api.py`
- [x] 1.2 In `TodoCreate.to_todo()`, validate `self.due` and normalize empty/None to `None`
- [x] 1.3 Ensure `ValueError` is raised for invalid or past due dates

## 2. Simplify API add_todo endpoint

- [x] 2.1 Remove redundant `validate_due_date` call and `todo.due` override in `add_todo`
- [x] 2.2 Wrap `todo_data.to_todo()` in try/except to return 422 on validation errors
- [x] 2.3 Keep `todo.user_id = current_user.id` assignment

## 3. Simplify web add_todo route

- [x] 3.1 Remove redundant `_validate_due_date` call in web `add_todo`
- [x] 3.2 Use `todo_data.to_todo()` and catch `ValueError` to re-render form with error

## 4. Add / update tests

- [x] 4.1 Add API test: `to_todo()` validates valid future due date
- [x] 4.2 Add API test: `to_todo()` normalizes empty string to `None`
- [x] 4.3 Add API test: `to_todo()` raises `ValueError` for invalid format
- [x] 4.4 Add API test: `to_todo()` raises `ValueError` for past date
- [x] 4.5 Add API test: `add_todo` returns 422 when `to_todo()` raises `ValueError`

## 5. Verify

- [x] 5.1 Run `pytest tests/test_api.py` to ensure all tests pass
- [x] 5.2 Run `pytest tests/test_web.py` to ensure web tests still pass
