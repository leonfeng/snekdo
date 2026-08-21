## Why

The E2E test `test_empty_login_credentials` fails because submitting the login form with empty credentials does not display validation error messages. The test expects error phrases ("must be at least", "required", "error", or "invalid") in the response, but the current implementation captures the page text before the navigation completes after form submission, so error messages from the server re-render are never visible.

## What Changes

- Fix the `test_empty_login_credentials` E2E test to properly wait for the page to update after form submission, so error messages from the server re-render are captured
- Ensure the login form validation errors are properly displayed when submitting empty credentials
- Add appropriate waits after HTMX/form submissions in E2E tests to capture server-rendered responses

## Capabilities

### New Capabilities

- `e2e-test-login`: fix test empty login credentials - ensure error messages are captured after form submission

### Modified Capabilities

- (None)

## Impact

- `tests/e2e/test_security.py::test_empty_login_credentials` - test timing fix to wait for page navigation after login form submission
- No changes to backend authentication logic required
- No new dependencies
