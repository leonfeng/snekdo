## 1. CSRF core module

- [ ] 1.1 Create `snekdo/csrf.py` with token generation (`secrets.token_urlsafe`), per-session get-or-create, and validation helpers
- [ ] 1.2 Add a "token invalidated" path so the stored token is cleared on logout

## 2. Web auth hardening

- [ ] 2.1 Replace the static default secret in `snekdo/web_auth.py` with an env-var-sourced key and random per-process fallback
- [ ] 2.2 Ensure plaintext passwords never appear in logs (log usernames only)

## 3. CSRF wiring into web routes

- [ ] 3.1 Validate the CSRF token on HTML form POSTs to state-changing web endpoints (login, register, add, edit, complete, delete, profile update, password change, account deletion) and reject with 403 on missing/mismatched token without mutating state
- [ ] 3.2 Skip CSRF validation for JSON / `HX-Request` requests so the REST API and HTMX JSON paths are unaffected

## 4. Templates carry the token

- [ ] 4.1 Add the CSRF hidden input to `snekdo/templates/` state-changing forms: add, edit, complete, delete row, profile_content, login, register

## 5. HTMX template fixes

- [ ] 5.1 Fix `snekdo/templates/list_row.html` / `list_rows.html` so a completed or deleted row swaps with valid HTML and sibling rows keep their HTMX wiring
- [ ] 5.2 Render the empty state as a `<p>` inside `<tbody>` when the last todo is deleted
- [ ] 5.3 Fix profile/password form HTMX targets to reference the inner container, not the form's own wrapper
- [ ] 5.4 Make delete-account and password-change HTMX responses return HTML, not a 302 redirect

## 6. E2E coverage

- [ ] 6.1 Add `tests/e2e/test_security.py` covering CSRF acceptance, missing-token rejection (403), mismatched-token rejection (403), and token invalidation on logout
- [ ] 6.2 Update `tests/e2e/conftest.py` to expose a helper that extracts the CSRF token from a rendered form for authenticated e2e requests
- [ ] 6.3 Update `tests/e2e/test_auth.py` to register/login through the web forms with the CSRF token and to assert no plaintext password appears in logs

## 7. Unit coverage

- [ ] 7.1 Add `tests/test_web.py` cases for the CSRF module (generation uniqueness, session stability, mismatch rejection) and for the secret fallback behavior
- [ ] 7.2 Run the full pytest suite and fix regressions caused by the changes

## 8. Documentation

- [ ] 8.1 Note the required secret environment variable and multi-worker implication in the README/AGENTS.md wiring notes