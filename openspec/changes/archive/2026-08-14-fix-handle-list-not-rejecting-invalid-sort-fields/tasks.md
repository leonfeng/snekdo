## 1. Update `handle_list` to reject invalid sort fields

- [x] 1.1 Add explicit validation of `args.sort` in `handle_list` so that values not in `["created_at", "title", "priority", "completed"]` produce an error message on stderr and return exit code 1.
- [x] 1.2 Ensure the error message lists the valid sort fields.

## 2. Add test coverage

- [x] 2.1 Add a test in `tests/test_cli.py` verifying that `handle_list` returns exit code 1 when `args.sort` is an invalid value.
- [x] 2.2 Add a test verifying the error message contains the valid sort field names.

## 3. Verify

- [x] 3.1 Run `pytest` to confirm all tests pass.
- [x] 3.2 Run `snekdo list --sort invalid_field` to confirm it returns a non-zero exit code and shows an error message.
