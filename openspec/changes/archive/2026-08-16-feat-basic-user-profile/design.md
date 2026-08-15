## Context

The snekdo project already has a `User` model in `snekdo/models.py`, a `UserStorage` class in `snekdo/storage.py`, and authentication endpoints in `snekdo/api_auth.py`. The FastAPI app in `snekdo/api.py` exposes todo CRUD endpoints protected by JWT authentication. The CLI in `snekdo/__main__.py` provides todo management commands plus register/login/logout.

## Goals / Non-Goals

**Goals:**
- Add `display_name` and `email` fields to the `User` model and storage layer.
- Add API endpoints for viewing and updating the authenticated user's profile.
- Add CLI commands for viewing and updating the profile.
- Allow password changes through the API and CLI.

**Non-Goals:**
- Account deletion (deletion is out of scope for "basic" profile).
- Password reset via email (only in-app password change with current password).
- Profile photo upload.
- Email verification flows.
- Social authentication.

## Decisions

### 1. Extend the existing `User` model

The `User` dataclass in `snekdo/models.py` will gain two optional fields:
- `display_name: str = ""` — the user's display name (default empty).
- `email: str = ""` — the user's email address (default empty).

These fields are added to `to_dict()` and `from_dict()` so they are persisted in `users.json`.

### 2. Use the existing `UserStorage` for profile operations

`UserStorage` in `snekdo/storage.py` already provides `add`, `get`, `get_by_id`, and `delete`. We add:
- `update(user_id, display_name=None, email=None)` — updates the display name and/or email of the user with the given ID.
- `update_password(user_id, current_password, new_password)` — verifies the current password hash and updates the password hash.

### 3. Add API endpoints in `snekdo/api.py`

Three new endpoints protected by `get_current_user`:
- `GET /api/v1/users/me` → returns the current user's profile (id, username, display_name, email, created_at).
- `PUT /api/v1/users/me` → updates display_name and/or email.
- `PUT /api/v1/users/me/password` → changes the password (requires current_password, new_password, confirm_password).

A new `UserUpdate` Pydantic model accepts optional `display_name` and `email`.
A new `PasswordChange` Pydantic model requires `current_password`, `new_password`, `confirm_password`.
A new `UserProfileResponse` Pydantic model includes `id`, `username`, `display_name`, `email`, `created_at`.

### 4. Add CLI commands in `snekdo/__main__.py`

Three new subcommands:
- `snekdo profile` — displays the current user's profile (requires stored credentials).
- `snekdo profile update --display-name "..." --email "..."` — updates the profile.
- `snekdo change-password --current-password "..." --new-password "..." --confirm-password "..."` — changes the password.

These commands use the `ServerHttpClient` to call the API endpoints.

### 5. Reuse existing authentication infrastructure

The existing `get_current_user` dependency extracts the user ID from the JWT token and looks up the user. This is reused for all profile endpoints. No changes to the JWT token claims are needed since the token already contains the user ID (`sub` claim).

## Risks / Trade-offs

- **Risk**: Adding `display_name` and `email` to the `User` model changes the `users.json` schema. Existing users.json files without these fields will still work because `from_dict` uses `.get()` with defaults.
- **Risk**: Password change requires storing the current password hash. The existing `verify_password` function is reused, so no new dependency is needed.
- **Trade-off**: Using `PUT /api/v1/users/me` for both create and update is not applicable here since users are created via `/api/v1/auth/register`. The profile endpoint is strictly an update.
- **Trade-off**: The CLI profile commands require the user to be logged in (stored credentials). If not logged in, an error is shown.

## Migration Plan

No migration script is needed. The `User.from_dict` method already handles missing `display_name` and `email` fields gracefully via `.get()` defaults. Existing `users.json` files will load without errors.

## Open Questions

- Should the email field be required or optional? **Assumption**: Optional (default empty string).
- Should the display name be required at registration? **Assumption**: Not required; users can set it later via profile update.
- Should the password change endpoint also accept a new password without the current password for "reset" flows? **Assumption**: No, this is a basic in-app password change that requires the current password.