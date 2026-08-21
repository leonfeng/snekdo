## Why

The snekdo application currently supports user registration, login, and JWT-based authentication, but users have no way to view or manage their account information after signing up. A basic user profile capability is needed so users can view their account details, update their profile information, and change their password.

## What Changes

- Add a new `user-profile` capability that provides endpoints/commands for viewing and updating the authenticated user's profile.
- The profile includes: username, email (optional), display name (optional), and account creation timestamp.
- Users can update their display name and email.
- Users can change their password (current password + new password).
- CLI support to view and modify the local user's profile.

## Capabilities

### New Capabilities

- `user-profile`: View and update the authenticated user's profile information, including display name, email, and password change.

### Modified Capabilities

<!-- No existing capabilities have requirement changes. The user-auth capability
already provides JWT tokens with the user ID, which is sufficient for profile
lookups. -->

## Impact

- Affected code: `snekdo/api.py` (new profile endpoints), `snekdo/models.py` (User model additions), `snekdo/storage.py` (user persistence), CLI subcommands in `snekdo/__main__.py`.
- APIs: New `GET /api/v1/users/me`, `PUT /api/v1/users/me`, `PUT /api/v1/users/me/password`.
- Dependencies: No new external dependencies; uses existing JWT/auth infrastructure.