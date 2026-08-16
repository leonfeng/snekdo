## Purpose

Defines the shared Playwright end-to-end test harness for the snekdo
HTMX/Jinja2 web frontend. Journey coverage lives in dedicated `e2e-*`
capabilities (auth, todos, profile, and account deletion).

## Requirements

### Requirement: E2E test harness boots a test server

The system SHALL provide an E2E test harness that starts a temporary FastAPI
test server and a Playwright browser context so tests can exercise the web UI
end-to-end without manual setup.

#### Scenario: Test server is reachable

- **WHEN** the E2E test harness is initialized
- **THEN** a FastAPI app with web routes is running on a local port and is
  reachable via `http://127.0.0.1:<port>`

#### Scenario: Browser context is available

- **WHEN** the E2E test harness is initialized
- **THEN** a Playwright browser context is available for navigation and
  interaction
