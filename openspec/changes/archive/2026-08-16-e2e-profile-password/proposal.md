## Why

Changing the password is a sensitive user action that requires careful E2E
testing to verify that users can update their password and receive appropriate
feedback for invalid input (wrong current password, too short, mismatched).

## What Changes

- Add E2E tests for changing the password in `tests/e2e/test_profile.py`

## Capabilities

### New Capabilities

- `e2e-profile-password`: End-to-end tests for changing the user password.