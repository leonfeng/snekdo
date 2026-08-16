## Context

This sub-change implements the E2E tests for completing a todo, as part of the
larger `chore-add-end-to-end-tests-for-web-frontend` change. The test server
fixture and Playwright browser context are shared across all E2E sub-changes.

## Scope

- Complete todo via HTMX updates row without full page reload
- Complete todo via redirect (no HTMX) redirects to list

## Dependencies

- `playwright` dev dependency (added in parent change)
- `tests/e2e/conftest.py` test server fixture
- `pytest-asyncio` for async test support