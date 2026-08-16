## Why

Viewing the profile page is a key user action. E2E tests verify that logged-in
users can view their profile information including username, display name,
email, and account creation date.

## What Changes

- Add E2E tests for the profile page in `tests/e2e/test_profile.py`

## Capabilities

### New Capabilities

- `e2e-profile-view`: End-to-end tests for viewing the user profile.