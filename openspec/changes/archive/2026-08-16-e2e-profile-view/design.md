## Context

This sub-change implements the E2E tests for viewing the user profile, as part
of the larger `chore-add-end-to-end-tests-for-web-frontend` change. The test
server fixture and Playwright browser context are shared across all E2E
sub-changes.

## Scope

- Profile page renders with user info (username, display name, email, created at)

## Dependencies

- `playwright` dev dependency (added in parent change)
- `tests/e2e/conftest.py` test server fixture
- `pytest-asyncio` for async test support