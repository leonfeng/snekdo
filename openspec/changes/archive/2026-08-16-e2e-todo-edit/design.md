## Context

This sub-change implements the E2E tests for editing a todo, as part of the
larger `chore-add-end-to-end-tests-for-web-frontend` change. The test server
fixture and Playwright browser context are shared across all E2E sub-changes.

## Scope

- Edit form pre-fills values
- Edit todo with valid update → redirect to list
- Edit todo with empty title → error message

## Dependencies

- `playwright` dev dependency (added in parent change)
- `tests/e2e/conftest.py` test server fixture
- `pytest-asyncio` for async test support