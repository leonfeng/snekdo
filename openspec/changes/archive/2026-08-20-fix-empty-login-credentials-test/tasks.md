## 1. Fix test timing

- [ ] 1.1 Add `await page.wait_for_load_state("load")` after form submission in `tests/e2e/test_security.py::test_empty_login_credentials`
- [ ] 1.2 Verify the test passes with the added wait

## 2. Verify the fix

- [ ] 2.1 Run `tests/e2e/test_security.py::test_empty_login_credentials` and confirm it passes
- [ ] 2.2 Run the full E2E test suite to ensure no regressions
