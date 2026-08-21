## Why

The web frontend has security gaps (missing CSRF protection, weak secrets management) and HTMX template bugs, with no end-to-end coverage for the auth/security flows. This adds a CSRF guard to state-changing web forms, hardens auth handling, fixes the HTMX/Jinja2 template bugs, and adds e2e coverage for auth and security flows.

## What Changes

- Add a CSRF token module (`snekdo/csrf.py`): generate per-session tokens and validate them on state-changing web endpoints.
- Enforce CSRF tokens on HTML form submissions (login, register, add, edit, complete, delete, profile updates) while leaving JSON/HTMX request paths unaffected.
- Harden web auth: strengthen secret handling and password policy in `snekdo/web_auth.py`.
- Fix HTMX template bugs in `snekdo/templates/` (list row rendering, list rows, edit, base layout, add, login, register, profile content) and `snekdo/web.py` request handling.
- Add e2e coverage: `tests/e2e/test_security.py` plus updates to `tests/e2e/conftest.py` and `tests/e2e/test_auth.py` so auth and security flows are exercised end-to-end.

## Capabilities

### New Capabilities

- `web-csrf-protection`: CSRF token generation, storage, and validation for state-changing web forms.

### Modified Capabilities

- `user-auth`: password/secret policy and auth flow requirements are tightened.
- `htmx-jinja2-frontend`: HTMX template rendering and interaction behavior requirements are corrected.

## Impact

- `snekdo/web.py` — wire CSRF validation into state-changing endpoints; fix HTMX/HTMX-target request handling.
- `snekdo/web_auth.py` — hardened secret handling and password policy.
- `snekdo/csrf.py` — new module (token generation/verification).
- `snekdo/templates/*.html` — add CSRF fields to forms; fix HTMX template bugs.
- `tests/e2e/` — new security e2e tests; conftest helpers to supply/verify CSRF tokens; updated auth e2e tests.
- Existing API (`/api/v1/*`) and CLI behavior are unchanged; CSRF applies to the HTML web app only.