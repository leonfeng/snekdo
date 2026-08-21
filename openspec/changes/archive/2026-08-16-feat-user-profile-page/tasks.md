## Tasks

### 1. Add profile route and template

- [x] 1.1 Create `snekdo/templates/profile.html` with a profile display and update forms.
- [x] 1.2 Add `GET /profile` route in `snekdo/web.py` that renders the profile page.
- [x] 1.3 Add a "Profile" link to `snekdo/templates/base.html` navigation bar.

### 2. Add profile update functionality

- [x] 2.1 Add `POST /profile/update` route in `snekdo/web.py` to handle profile updates.
- [x] 2.2 Validate email format and display errors.
- [x] 2.3 Update user data via `UserStorage`.
- [x] 2.4 Use HTMX for partial page update of the profile display.

### 3. Add password change functionality

- [x] 3.1 Add `POST /profile/password` route in `snekdo/web.py` to handle password changes.
- [x] 3.2 Verify current password.
- [x] 3.3 Validate new password length (min 8 chars) and confirmation match.
- [x] 3.4 Update password via `UserStorage`.
- [x] 3.5 Display success or error messages.

### 4. Testing

- [x] 4.1 Add tests for the profile page route.
- [x] 4.2 Add tests for profile update.
- [x] 4.3 Add tests for password change.
- [x] 4.4 Add tests for unauthenticated access protection.

### 5. Verification

- [x] 5.1 Run the test suite to verify all tests pass.
- [x] 5.2 Manually verify the profile page renders correctly.
- [x] 5.3 Verify HTMX partial updates work on the profile page.
