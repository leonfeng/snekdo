## Context

The E2E test `test_empty_login_credentials` in `tests/e2e/test_security.py` fails because submitting the login form with empty credentials does not display validation error messages. The test expects error phrases ("must be at least", "required", "error", or "invalid") in the response text, but the current implementation captures the page text before the navigation completes after form submission.

This is a test timing issue, not a backend authentication problem. The login form validation and error rendering are working correctly - the issue is that the test's `page.evaluate(() => form.submit())` causes a page navigation, and `_get_text(page)` is called immediately after without waiting for the navigation to complete.

## Goals / Non-Goals

**Goals:**
- Fix the `test_empty_login_credentials` E2E test to properly capture error messages after login form submission
- Add appropriate waits after form submissions in E2E tests to ensure server-rendered responses are fully rendered
- Ensure the test reliably validates that login form error messages are displayed

**Non-Goals:**
- Modify the backend authentication logic
- Change the login form validation behavior
- Fix other E2E tests that may have similar timing issues

## Decisions

- The fix is a test timing improvement, not a behavior change
- Add `await page.wait_for_load_state("load")` or `await page.wait_for_timeout(500)` after form submission in the failing test
- The login backend validation (`snekdo/web_auth.py`) correctly returns error messages for empty credentials - no changes needed there

## Risks / Trade-offs

- Minimal risk: this is a test timing fix only
- The change is isolated to the E2E test file
- No impact on production code or API behavior

## Migration Plan

- Apply the test fix to `tests/e2e/test_security.py::test_empty_login_credentials`
- Run the test suite to verify the fix works
- No data migration or rollback strategy needed

## Open Questions

- None - this is a straightforward test timing fix
