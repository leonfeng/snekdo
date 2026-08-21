## 1. Fix web edit form to preserve due date

- [x] 1.1 In `snekdo/web.py` `edit_todo`, only pass `due` to `storage.modify()` when `due_clean` is not `None`
- [x] 1.2 In `snekdo/web.py` `edit_todo`, handle `ValueError` from `validate_due_date` and render the edit form with an error

## 2. Fix CLI modify handler to handle None return value

- [x] 2.1 In `snekdo/__main__.py` `handle_modify`, change the `is not None` check to a truthy check for `args.due`
- [x] 2.2 In `snekdo/__main__.py` `handle_add`, verify that `validate_due_date` `None` return is stored correctly (no change needed, but verify)

## 3. Fix API modify handler to handle None return value

- [x] 3.1 In `snekdo/api.py` `modify_todo`, change the `is not None` check to a truthy check for `update_data.due`
- [x] 3.2 In `snekdo/api.py` `TodoCreate.to_todo`, verify that `validate_due_date` `None` return is stored correctly (no change needed, but verify)

## 4. Update specs

- [x] 4.1 Create `specs/web-edit-due-date/spec.md` with new requirements
- [x] 4.2 Update `specs/todo-modification/spec.md` with delta requirements
- [x] 4.3 Update `specs/api-due-date-completed/spec.md` with delta requirements

## 5. Verify

- [x] 5.1 Run `openspec validate` to check the change
- [x] 5.2 Run the test suite to ensure no regressions (278 passed)
