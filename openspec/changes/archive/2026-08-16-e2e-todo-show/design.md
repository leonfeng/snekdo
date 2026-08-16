## Context

This sub-change implements the E2E tests for showing todo details, as part of
the larger `chore-add-end-to-end-tests-for-web-frontend` change. The test server
fixture and Playwright browser context are shared across all E2E sub-changes.

## Scope

- Show todo details page displays title, description, due date, priority, status, created at
- Non-existent todo shows 404

## Dependencies

- `playwright` dev dependency (added in parent change)
- `tests/e2e/conftest.py` test server fixture
- `pytest-asyncio` for async test support