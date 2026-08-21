## 1. E2E security tests

- [x] 1.1 Add `tests/e2e/test_security.py` covering CSRF acceptance on a valid token, missing-token rejection (403), mismatched-token rejection (403), and no state mutation on rejection

## 2. E2E token invalidation

- [x] 2.1 Add a test asserting the CSRF token is invalidated on logout (resubmitting the pre-logout token is rejected)

## 3. Conftest helper

- [x] 3.1 Update `tests/e2e/conftest.py` to expose a helper that extracts the CSRF token from a rendered form for authenticated e2e requests

## 4. Web auth e2e flows

- [x] 4.1 Update `tests/e2e/test_auth.py` to register and login through the web forms with the CSRF token

## 5. Log assertion

- [x] 5.1 Add an assertion that no plaintext password appears in logs during register/login

## 6. Verification

- [x] 6.1 Run the e2e suite and confirm the new tests pass against the applied CSRF and HTMX changes