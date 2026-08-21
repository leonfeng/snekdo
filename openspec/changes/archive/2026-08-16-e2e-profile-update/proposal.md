## Why

Updating the profile (display name and email) is a key user action. E2E tests
verify that users can update their information and receive appropriate feedback
for invalid input.

## What Changes

- Add E2E tests for updating the profile in `tests/e2e/test_profile.py`

## Capabilities

### New Capabilities

- `e2e-profile-update`: End-to-end tests for updating the user profile.