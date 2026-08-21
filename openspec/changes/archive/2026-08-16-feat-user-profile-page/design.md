## Design

### Overview

Add a `/profile` web route to the existing Jinja2/HTMX frontend that lets authenticated users view and manage their profile. The backend already has the necessary API endpoints (`GET/PUT /api/v1/users/me`, `PUT /api/v1/users/me/password`) defined in the `user-profile` spec, so the change is primarily a frontend addition.

### Architecture

The profile page reuses the existing `UserStorage` to fetch the current user's data and the existing `TodoStorage` for todo operations. The page is protected by the `_require_login` dependency that reads the token from cookies.

### Implementation Plan

1. **Add profile route** (`GET /profile`) in `snekdo/web.py`:
   - Use `_require_login` to protect the route.
   - Fetch the current user from `UserStorage`.
   - Render `profile.html` with the user's profile data.

2. **Add profile update route** (`PUT /profile` or `POST /profile`):
   - Use `_require_login` to protect the route.
   - Read form data for `display_name` and `email`.
   - Validate the email format.
   - Call `UserStorage.update()` to update the user.
   - Return a partial page update (HTMX) or redirect.

3. **Add password change route** (`PUT /profile/password` or `POST /profile/password`):
   - Use `_require_login` to protect the route.
   - Read form data for `current_password`, `new_password`, `confirm_password`.
   - Verify the current password.
   - Validate the new password length and confirmation match.
   - Update the password in `UserStorage`.
   - Return a success message or error.

4. **Create profile template** (`snekdo/templates/profile.html`):
   - Display the user's profile information.
   - Include a form for updating display name and email.
   - Include a separate form for changing password.
   - Use HTMX for form submissions.

5. **Update navigation bar** (`snekdo/templates/base.html`):
   - Add a "Profile" link to the navigation bar.

### Key Decisions

- The profile page uses the existing `UserStorage` class (not the API) for direct data access, consistent with how the todo list page uses `TodoStorage`.
- Form submissions use HTMX `hx-post`/`hx-put` for partial page updates, matching the existing frontend pattern.
- Validation is done server-side, with errors displayed on the page.
- The password change form is separate from the profile update form for security (requires current password).

### File Changes

| File | Change |
|------|--------|
| `snekdo/web.py` | Add `/profile`, `/profile/update`, `/profile/password` routes |
| `snekdo/templates/profile.html` | New file: profile page template |
| `snekdo/templates/base.html` | Add "Profile" link to navigation |

### Dependencies

- `snekdo/storage.py` — `UserStorage` for user data access.
- `snekdo/auth.py` — password hashing/verification.
- `snekdo/web_auth.py` — existing auth web routes.
