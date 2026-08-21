## Why

The login flow is a critical user journey that needs end-to-end browser testing
to verify that existing users can authenticate and receive appropriate feedback
for invalid credentials.

## What Changes

- Add E2E tests for login in `tests/e2e/test_auth.py`

## Capabilities

### New Capabilities

- `e2e-auth-login`: End-to-end tests for the user login flow.