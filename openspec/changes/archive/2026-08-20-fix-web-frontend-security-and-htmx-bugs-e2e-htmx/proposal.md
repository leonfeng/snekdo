## Why

The HTMX/Jinja2 template interactions have bugs: the completed/deleted row swap can drop sibling rows' HTMX wiring, the empty state after deleting the last todo can emit invalid HTML, and the profile/password forms target their own wrapper causing self-referential replacement. This fixes the template interactions so partial updates stay valid and interactive.

## What Changes

- Fix `snekdo/templates/list_row.html` / `list_rows.html` so a completed or deleted row swaps with valid HTML and the remaining rows keep their HTMX wiring.
- Render the empty state after deleting the last todo as a `<p>` element inside the `<tbody>` (never `outerHTML` of a `<tr>`).
- Fix profile update and password change form HTMX targets to reference the inner container, not the form's own wrapper.
- Make delete-account and password-change HTMX responses return HTML content, not a 302 redirect, so the page updates in place.

Assumes the CSRF change (`fix-web-frontend-security-and-htmx-bugs-e2e-csrf`) has been applied; forms already carry the token.

## Capabilities

### New Capabilities

(None)

### Modified Capabilities

- `htmx-jinja2-frontend`: complete/delete behavior, empty-state HTML, and profile/password HTMX targets must stay valid across partial updates.

## Impact

- `snekdo/templates/list_row.html`, `list_rows.html` — row swap fragment and empty-state HTML.
- `snekdo/templates/profile_content.html` — HTMX target fixes for profile update and password change.
- `snekdo/web.py` — delete-account / password-change routes return HTML for HTMX requests instead of a 302 redirect.
- No changes to the REST API, CLI, or storage. No new dependencies.