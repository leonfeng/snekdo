## Why

The registration flow is a critical user journey that needs end-to-end browser
testing to verify that new users can create an account and receive appropriate
feedback for invalid input.

## What Changes

- Add E2E tests for registration in `tests/e2e/test_auth.py`

## Capabilities

### New Capabilities

- `e2e-auth-registration`: End-to-end tests for the user registration flow.