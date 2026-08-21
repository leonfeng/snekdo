## Why

E2E test `test_registration_with_invalid_data` in `tests/e2e/test_auth.py` fails when registering a user with invalid data. The test submits registration with invalid username or password, but the error handling does not properly render the validation error message in the response. The assertion expecting "invalid csrf token" or similar error message fails because the page content does not contain the expected error text.

## What Changes

- Fix registration validation error rendering in the auth routes/templates
- Ensure invalid registration data produces appropriate error messages visible in the UI
- Fix the assertion logic in `test_registration_with_invalid_data` to correctly capture error output

## Capabilities

### New Capabilities

- `e2e/test-auth`: Fix registration validation error handling in tests/e2e/test_auth.py and associated auth templates

### Modified Capabilities

- (none - no existing spec requirements changing)

## Impact

- 1 E2E test in `tests/e2e/test_auth.py` will pass
- Auth registration error handling improvements
- No API changes needed - test and template fixes
