## Why

The logout flow is a critical user journey that needs end-to-end browser testing
to verify that logged-in users can invalidate their session and are redirected
to the login page.

## What Changes

- Add E2E tests for logout in `tests/e2e/test_auth.py`

## Capabilities

### New Capabilities

- `e2e-auth-logout`: End-to-end tests for the user logout flow.