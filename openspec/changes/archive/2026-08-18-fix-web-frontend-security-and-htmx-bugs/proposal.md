## Why

The HTMX/Jinja2 web frontend introduced in the user-account feature has several security and correctness bugs: no CSRF protection on any form, invalid HTML when deleting the last todo, stale-object attribute writes, unhandled Pydantic v2 validation errors, and an insecure GET logout. These bugs affect both the `htmx-jinja2-frontend` and `user-auth` capabilities and need to be fixed before the feature is considered complete.

## What Changes

- Add CSRF token generation and validation for all web forms (add, edit, complete, delete, profile, password, account deletion, login, register).
- Fix the delete-todo HTMX swap so the empty state renders as a `<p>` within the `<tbody>` (not as `outerHTML` of a `<tr>`).
- Fix the complete-todo handler to not set a stale object attribute on a previously-loaded instance.
- Catch Pydantic v2 `ValidationError` in add/edit todo handlers so invalid input re-renders the form with HTML errors instead of a 422 JSON response.
- Replace the `Form(..., min_length=...)` login validation with manual `ValueError`/`ValidationError` so login failures re-render the form with HTML errors.
- Change the logout route from GET to POST so it is not cacheable/CSRF-able.
- Make the delete-account handler respect HTMX requests by returning HTML rather than a 302 redirect.
- Add allowed-values validation for the add-todo priority Form field.
- Clarify and fix empty-string due-date handling in the edit-todo handler.
- Add e2e tests covering the new behavior (CSRF, last-todo delete, invalid priority, empty login, logout).

## Capabilities

### New Capabilities

- `web-csrf`: CSRF token generation and validation for all web forms and state-changing requests.

### Modified Capabilities

- `htmx-jinja2-frontend`: Delete/complete/edit/add todo HTMX behavior, empty-state rendering, and error handling.
- `user-auth`: Login validation, logout method, and account-deletion HTMX handling.

## Impact

- Affected code: `snekdo/web.py`, `snekdo/web_auth.py`, `snekdo/templates/*.html`, `snekdo/session.py` (new CSRF token utility), `tests/e2e/`.
- No new dependencies; CSRF tokens are generated with `secrets.token_hex` and stored in the session.
- Breaking: logout changes from GET to POST; existing links/bookmarks to `/auth/logout` will break.