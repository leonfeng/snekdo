## Why

The user authentication web frontend has several bugs: login and registration validation returns JSON 422 responses instead of re-rendering the form with HTML errors, the logout route uses GET (which is cacheable and CSRF-able), and the account deletion handler does not properly handle HTMX requests.

## What Changes

- Replace FastAPI `Form(..., min_length=...)` login validation with manual `ValueError`/`ValidationError` so login failures re-render the form with HTML errors.
- Change the logout route from GET to POST so it is not cacheable/CSRF-able.
- Update templates to use a POST form for logout.
- Make the delete-account handler respect HTMX requests by returning HTML rather than a 302 redirect (handled in the `htmx-jinja2-frontend` child change).

## Capabilities

### Modified Capabilities

- `user-auth`: Login validation, logout method, and account-deletion HTMX handling.

## Impact

- Affected code: `snekdo/web_auth.py`, `snekdo/templates/*.html`.
- No new dependencies.
- The CSRF token generation/invalidation is handled by the `web-csrf` child change.
- The delete-account HTMX handling is handled by the `htmx-jinja2-frontend` child change.
- **BREAKING**: Logout changes from GET to POST.