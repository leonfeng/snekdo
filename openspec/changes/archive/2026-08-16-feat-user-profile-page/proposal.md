## Why

The snekdo web frontend currently provides authentication (login/register) and full todo CRUD operations, but authenticated users have no way to view or manage their account profile through the browser. The `user-profile` API capability already exposes the necessary endpoints (`GET/PUT /api/v1/users/me`, `PUT /api/v1/users/me/password`), but these are only accessible via direct HTTP calls. Users need a convenient web page to view their profile, update their display name and email, and change their password.

## What Changes

- Add a new web route `GET /profile` that displays the authenticated user's profile information (username, display name, email, created_at).
- Add a web form to update the user's display name and/or email via `PUT /api/v1/users/me`.
- Add a password change form at `PUT /api/v1/users/me/password` accessible from the profile page.
- Add a `/profile` link in the navigation bar.
- Protect the profile page with the existing login requirement.
- Use HTMX for partial page updates on profile updates.

## Capabilities

### New Capabilities

- `user-profile-page`: Web-based profile page that lets authenticated users view their profile, update display name and email, and change password through the Jinja2/HTMX frontend.

### Modified Capabilities

- None (the existing `user-profile` API spec covers the backend endpoints; this change only adds the web frontend layer).

## Impact

- `snekdo/web.py`: Add new profile routes and form handling.
- `snekdo/templates/profile.html`: New template for the profile page.
- `snekdo/templates/base.html`: Add a "Profile" link to the navigation bar.
- `snekdo/api_client.py`: Optionally add a client method for profile operations (if needed by CLI).
- Frontend-only change; no new API endpoints or database schema changes.
