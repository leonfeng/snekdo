## Why

The auth and security flows (login, register, logout, CSRF acceptance/rejection, token invalidation) lack end-to-end coverage. This adds e2e tests that exercise the web auth forms and CSRF guard through the real request cycle, so regressions are caught at the integration boundary.

## What Changes

- Add `tests/e2e/test_security.py` covering CSRF acceptance, missing-token rejection (403), mismatched-token rejection (403), and CSRF token invalidation on logout.
- Update `tests/e2e/conftest.py` to expose a helper that extracts the CSRF token from a rendered form for authenticated e2e requests.
- Update `tests/e2e/test_auth.py` to register/login through the web forms with the CSRF token and to assert no plaintext password appears in logs.

Assumes both the CSRF change and the HTMX change have been applied. This change is test-only and does not modify production behavior.

## Impact

- `tests/e2e/test_security.py` — new.
- `tests/e2e/conftest.py` — CSRF-token-extraction helper.
- `tests/e2e/test_auth.py` — token-aware web auth flows + no-plaintext-password-in-logs assertion.
- No production code, REST API, CLI, or spec changes.