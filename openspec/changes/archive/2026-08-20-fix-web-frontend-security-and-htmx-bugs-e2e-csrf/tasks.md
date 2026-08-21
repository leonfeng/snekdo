## 1. CSRF core module

- [x] 1.1 Create `snekdo/csrf.py` with token generation (`secrets.token_urlsafe`), per-session get-or-create, and validation helpers
- [x] 1.2 Add a "token invalidated" path so the stored token is cleared on logout

## 2. Web auth hardening

- [x] 2.1 Replace the static default secret in `snekdo/web_auth.py` with an env-var-sourced key and random per-process fallback
- [x] 2.2 Ensure plaintext passwords never appear in logs (log usernames only)

## 3. CSRF wiring into web routes

- [x] 3.1 Validate the CSRF token on HTML form POSTs to state-changing web endpoints (login, register, add, edit, complete, delete, profile update, password change, account deletion) and reject with 403 on missing/mismatched token without mutating state
- [x] 3.2 Skip CSRF validation for JSON / `HX-Request` requests so the REST API and HTMX JSON paths are unaffected

## 4. Templates carry the token

- [x] 4.1 Add the CSRF hidden input to `snekdo/templates/` state-changing forms: add, edit, complete, delete row, profile_content, login, register

## 5. Unit coverage

- [x] 5.1 Add `tests/test_web.py` cases for the CSRF module (generation uniqueness, session stability, mismatch rejection) and for the secret fallback behavior
- [x] 5.2 Run the full pytest suite and fix regressions caused by the changes

## 6. Documentation

- [x] 6.1 Note the required secret environment variable and multi-worker implication in the README/AGENTS.md wiring notes