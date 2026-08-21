## Why

The snekdo HTMX/Jinja2 web frontend currently has no CSRF protection on any form or state-changing request. This makes all web forms (add, edit, complete, delete, profile, password, account deletion, login, register) vulnerable to cross-site request forgery attacks. A CSRF token generation and validation mechanism must be added before the feature can be considered complete.

## What Changes

- Add `get_csrf_token()` helper to generate and store a CSRF token in the user's session.
- Add `verify_csrf_token()` helper to validate the CSRF token from incoming requests.
- Generate and rotate the CSRF token on login and registration.
- Include the CSRF token as a hidden input in all web forms via a template variable.
- Add CSRF validation to all POST/PUT/DELETE web routes (add, edit, complete, delete, profile, password, account deletion, login, register).
- Invalidate the CSRF token on logout.
- **BREAKING**: Logout changes from GET to POST (handled in the auth child change).

## Capabilities

### New Capabilities

- `web-csrf`: CSRF token generation, storage, validation, rotation, and invalidation for all web forms and state-changing requests.

### Modified Capabilities

- `htmx-jinja2-frontend`: Forms now include CSRF tokens; state-changing handlers validate CSRF.
- `user-auth`: Login/register generate/rotate CSRF tokens; logout invalidates CSRF token.

## Impact

- Affected code: `snekdo/session.py` (new CSRF utility), `snekdo/web.py`, `snekdo/web_auth.py`, `snekdo/templates/*.html`.
- No new dependencies; CSRF tokens are generated with `secrets.token_hex(32)` and stored in the session.
- Breaking: logout changes from GET to POST (see auth child change).