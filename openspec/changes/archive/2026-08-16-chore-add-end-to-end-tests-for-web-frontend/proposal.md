## Why

The snekdo web frontend currently only has unit tests using FastAPI's `TestClient`, which exercise route handlers in isolation but do not verify the full user journey through a real browser (HTML rendering, HTMX interactions, form submission, redirects, authentication flows). Adding end-to-end (E2E) tests gives confidence that the web UI works as a complete system in a real browser, matching the requirements in the `htmx-jinja2-frontend` spec.

## What Changes

- Add a Playwright-based E2E test suite for the web frontend, covering the full user journeys: registration, login, logout, listing todos, adding a todo, editing a todo, completing a todo, deleting a todo, viewing todo details, and updating the user profile / changing password.
- Add Playwright as a dev dependency.
- Add a `Makefile` target or `pytest` integration to run E2E tests, plus a small fixture that boots a test server and provides a browser context.
- No changes to production code behavior; this is a testing addition only.

## Capabilities

### New Capabilities

- `web-e2e-tests`: End-to-end browser tests for the HTMX/Jinja2 web frontend, covering all user-facing web routes and interactions defined in the `htmx-jinja2-frontend` spec.

### Modified Capabilities

<!-- No existing capability requirements change; the htmx-jinja2-frontend spec already
describes the behavior. This change adds a new test capability that verifies it. -->

## Impact

- Affected code: `tests/e2e/` (new E2E test files), `pyproject.toml` (add `playwright` dev dependency), `Makefile` (optional E2E target), `pytest.ini` (optional E2E config).
- Dependencies: `playwright` (browser testing framework) and its browser binaries.
- No changes to the API, CLI, storage, or web route implementations.
