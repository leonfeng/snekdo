## Why

The web frontend has no CSRF protection and `web_auth.py` falls back to a static hardcoded secret. This adds a per-session CSRF guard to state-changing web endpoints and hardens web auth secret handling, so cross-origin forgeries are rejected and no static secrets ship in the package.

## What Changes

- Add a CSRF token module (`snekdo/csrf.py`): per-session token generation (`secrets.token_urlsafe`), get-or-create, validation, and invalidation on logout.
- Enforce CSRF token validation on HTML form POSTs to state-changing web endpoints (login, register, add, edit, complete, delete, profile update, password change, account deletion); reject with 403 with no state mutation. JSON/`HX-Request` requests bypass CSRF validation.
- Add the CSRF hidden input to the state-changing web forms in `snekdo/templates/`.
- Harden `snekdo/web_auth.py`: replace the static default secret with an env-var-sourced key with a random per-process fallback; never log plaintext passwords.
- Add unit tests for the CSRF module and secret fallback behavior in `tests/test_web.py`.

## Capabilities

### New Capabilities

- `web-csrf-protection`: CSRF token generation, storage, and validation for state-changing web endpoints.

### Modified Capabilities

- `user-auth`: password/secret policy — no hardcoded default secret, no plaintext password logging.

## Impact

- `snekdo/web.py` — CSRF validation wired into state-changing web endpoints; JSON/HX path unaffected.
- `snekdo/web_auth.py` — secret sourced from env with random fallback; no password logging.
- `snekdo/csrf.py` — new module.
- `snekdo/templates/{add,edit,login,register,profile_content,list_row}.html` — hidden CSRF input added (templates only; HTMX behavior fixes are a later change).
- `tests/test_web.py` — unit coverage for the CSRF module and secret fallback.
- REST API and CLI behavior unchanged. Template HTMX interaction fixes and e2e coverage are separate changes.