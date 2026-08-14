## 1. Add validation helper

- [x] 1.1 Create a `validate_due_date` helper function in `snekdo/__main__.py`

## 2. Update add command

- [x] 2.1 Call `validate_due_date` in `handle_add` and reject invalid dates
- [x] 2.2 Update existing tests that use invalid dates

## 3. Update modify command

- [x] 3.1 Call `validate_due_date` in `handle_modify` and reject invalid dates
- [x] 3.2 Add test for modify command validation

## 4. Add tests

- [x] 4.1 Add test for valid date accepted
- [x] 4.2 Add test for invalid date format rejected
- [x] 4.3 Add test for past date rejected
- [x] 4.4 Add test for empty/omitted due date accepted

## 5. Verify

- [x] 5.1 Run `pytest` to ensure all tests pass
