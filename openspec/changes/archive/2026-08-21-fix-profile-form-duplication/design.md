# Design: Profile Form Duplication Fix

## Context

The profile page at `/profile` renders user information and three forms (Update Profile, Change Password, Delete Account) using HTMX for partial updates. The `profile_content.html` template contained both the profile info display and all forms. When the Update Profile form was submitted via `hx-post="/profile/update"`, the `update_profile` endpoint returned the full template, and HTMX's `hx-swap="outerHTML"` replaced `.profile-info` with the entire response, causing the forms to appear after the updated profile info and duplicate on repeated clicks.

## Goals

- Separate profile info display from forms to prevent HTMX duplication
- Maintain all existing functionality (update profile, change password, delete account)
- No breaking changes to API or behavior

## Non-Goals

- No new features or API changes
- No database schema changes
- No new dependencies

## Decisions

1. **Create `profile_info.html`**: Extracted profile info display (username, display_name, email, created_at) into its own partial template with all fields disabled
2. **Modify `profile_content.html`**: Now only includes `profile_info.html` — no forms
3. **Create `profile_forms.html`**: New template containing only the three forms, each with `hx-target=".profile-info" hx-swap="outerHTML"`
4. **Modify `profile.html`**: Includes both `profile_content.html` and `profile_forms.html`

This ensures HTMX submissions receive only the updated profile info div, preventing duplication.

## Risks / Trade-offs

- Low risk: template-only change, no logic modifications
- All existing tests should continue to pass
- If HTMX attributes change in the future, forms may need updating

## Open Questions

None — this is a straightforward template refactor with clear before/after states.
