## Context

This sub-change implements the E2E tests for the user login flow, as part of the
larger `chore-add-end-to-end-tests-for-web-frontend` change. The test server
fixture and Playwright browser context are shared across all E2E sub-changes.

## Scope

- Login with valid credentials → redirect to todo list
- Login with invalid credentials → error message

## Dependencies

- `playwright` dev dependency (added in parent change)
- `tests/e2e/conftest.py` test server fixture
- `pytest-asyncio` for async test support