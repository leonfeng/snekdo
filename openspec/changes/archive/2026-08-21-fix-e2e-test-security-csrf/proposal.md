## Why

Three E2E security tests in `tests/e2e/test_security.py` are failing:

1. **test_csrf_mismatched_token_rejection_403**: Submitting a form with a wrong CSRF token does not return 403 with "invalid csrf token" error message. The CSRF token cookie is not being properly read or the form submission doesn't include the token correctly, causing validation to pass or the page to redirect instead of showing an error.

2. **test_invalid_priority_on_add**: Adding a todo with an invalid priority (e.g., "urgent") appended dynamically to the select element causes a Playwright evaluation error. The JavaScript execution fails when trying to create and select a new option.

3. **test_csrf_token_invalidated_on_logout**: After logging out, the CSRF token cookie is not properly invalidated, causing subsequent requests to fail or behave unexpectedly.

## What Changes

- Fix CSRF token handling in form submissions to ensure mismatched tokens are properly rejected with 403
- Fix dynamic priority option creation in the add todo form to work with Playwright's DOM
- Fix CSRF token cookie invalidation on logout to properly clear the token

## Capabilities

### New Capabilities

- `e2e/test-security`: Fix CSRF token validation and logout token invalidation in tests/e2e/test_security.py
- `e2e/test-security`: Fix dynamic priority option handling in add todo form

### Modified Capabilities

- (none - no existing spec requirements changing)

## Impact

- 3 E2E tests in `tests/e2e/test_security.py` will pass
- CSRF protection improvements to the web frontend
- No API changes needed - test infrastructure and frontend fixes
