## 1. Create shared due-date utility module

- [x] 1.1 Create `snekdo/due_date.py` with `validate_due_date()` function
- [x] 1.2 Ensure the module imports only `datetime` (no `snekdo.*` imports)

## 2. Update CLI entry point

- [x] 2.1 Remove local `validate_due_date` definition from `snekdo/__main__.py`
- [x] 2.2 Add `from snekdo.due_date import validate_due_date` import

## 3. Update API module

- [x] 3.1 Remove `_validate_due_date` helper from `snekdo/api.py`
- [x] 3.2 Add `from snekdo.due_date import validate_due_date` import
- [x] 3.3 Update callers to use `validate_due_date` (already imported)

## 4. Update web frontend module

- [x] 4.1 Remove `_validate_due_date` helper from `snekdo/web.py`
- [x] 4.2 Add `from snekdo.due_date import validate_due_date` import

## 5. Verify and test

- [x] 5.1 Verify `snekdo serve` starts without circular import errors
- [x] 5.2 Run the test suite to confirm no regressions
