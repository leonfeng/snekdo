## Context

snekdo has a Jinja2 + HTMX web frontend (`snekdo/web.py`, `snekdo/templates/`)
served alongside the REST API on the same FastAPI server. Existing tests in
`tests/test_web.py` use FastAPI's `TestClient` to exercise route handlers in
isolation. There is no browser-based end-to-end test coverage.

## Goals / Non-Goals

**Goals:**
- Add a Playwright-based E2E test suite that exercises the full web UI in a
  real browser.
- Provide a test fixture that boots a temporary FastAPI server and a Playwright
  browser context, reusing the existing `create_app` / `register_web_routes`
  machinery.
- Cover all user-facing web routes: auth (register/login/logout), todo CRUD,
  show, complete, delete, and profile (view/update/password).

**Non-Goals:**
- No changes to production web route behavior.
- No changes to the CLI, API, or storage layers.
- No E2E tests for the CLI or the REST API (those are covered by unit tests).
- No mobile browser testing; desktop Chromium is sufficient.

## Decisions

### 1. Use Playwright

Playwright is the established standard for Python E2E testing and provides a
clean `async` API with auto-waiting. It is added as a dev dependency
(`playwright` package + `playwright install` for browser binaries).

### 2. E2E tests live under `tests/e2e/`

The existing `tests/` directory holds unit tests. E2E tests are placed in
`tests/e2e/` to keep them separate and allow them to be run with a targeted
command like `pytest tests/e2e/`.

### 3. Test server via a shared fixture

A `tests/e2e/conftest.py` fixture will:
- Create a temporary storage directory (like the existing `test_web.py`
  `client` fixture).
- Build the FastAPI app with `create_app(storage_path=...)` and register web
  routes.
- Use `pytest-asyncio` + a lightweight ASGI server (or `requests`/`httpx` to
  avoid extra process complexity) so the test server runs in-process.
- Provide a Playwright `Page` object for each test.

To keep things simple and avoid a separate server process, the E2E tests will
use Playwright's `request` context to make HTTP assertions and a headless
browser to verify HTML rendering. This avoids the need for `uvicorn` subprocess
management while still exercising the full request→response cycle.

### 4. One spec file per user journey

The E2E test suite is organized by user journey (auth, todos, profile) so that
each scenario in the `web-e2e-tests` spec maps to a clear test function.

### 5. Headless Chromium for CI

Tests run in headless Chromium by default. Playwright's `browserType.launch`
with `headless=True` is used so they work in CI without a display.

## Risks / Trade-offs

- **Risk**: Playwright browser binaries are large and may not be available in
  the sandbox. **Mitigation**: Use `playwright install chromium` in the CI step;
  the test harness degrades gracefully if no browser is installed by skipping
  E2E tests (marked `pytestmark` with a skip condition).
- **Risk**: In-process server may block on long-running tests. **Mitigation**:
  Each test uses a fresh temporary storage file and a fresh page context.
- **Trade-off**: Using an in-process server rather than a separate `uvicorn`
  process simplifies the fixture but means the E2E tests exercise the same
  ASGI app as the unit tests. This is acceptable because the goal is to verify
  the rendered HTML and user flows, not load testing.

## Migration Plan

- Add `playwright` to `[project.optional-dependencies]` → `dev` in `pyproject.toml`.
- Create `tests/e2e/conftest.py` with the test server + browser fixture.
- Create `tests/e2e/test_auth.py`, `tests/e2e/test_todos.py`,
  `tests/e2e/test_profile.py`.
- No migration of existing data is needed.

## Open Questions

- Should E2E tests be run in the default `pytest` invocation or gated behind a
  marker like `pytest -m "e2e"`? **Assumption**: gated behind a custom marker
  `e2e` so the fast unit-test suite is not slowed down.
- Should the test server run on a fixed port or a dynamic port? **Assumption**:
  dynamic port via `pytest-asyncio` fixture with `httpx` base URL injection.
