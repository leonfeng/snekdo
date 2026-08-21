# Profile Form Duplication Fix

## Why

The profile page's Update Profile form, when submitted via HTMX, was causing the profile information and forms to duplicate on repeated clicks. This occurred because `profile_content.html` contained both the profile info display and all three forms (Update Profile, Change Password, Delete Account). When HTMX swapped `.profile-info` with the full template response, the forms appeared after the updated profile info, and repeated clicks compounded the duplication.

## What Changes

- **Refactor profile templates** to separate profile info display from forms
- **Create `profile_info.html`**: Contains only the profile information display (username, display_name, email, created_at - all disabled)
- **Modify `profile_content.html`**: Now only includes `profile_info.html`
- **Create `profile_forms.html`**: Contains only the three forms (Update Profile, Change Password, Delete Account)
- **Modify `profile.html`**: Includes both `profile_content.html` and `profile_forms.html`

This ensures that when HTMX submits the Update Profile form, it receives only the updated profile info div without the forms, preventing duplication on repeated submissions.

## Capabilities

### New Capabilities
- `web/profile`: Frontend template restructuring for profile page

### Modified Capabilities
- None (pure template refactor, no behavior change at spec level)

## Impact

- **Templates**: `snekdo/templates/profile.html`, `profile_content.html`, `profile_forms.html`, `profile_info.html`
- **No API changes**, no database schema changes, no new dependencies

## Verification

- E2E tests confirm profile page loads correctly
- HTMX form submissions no longer cause duplication
- All profile-related functionality (update, password change, account delete) works as before
