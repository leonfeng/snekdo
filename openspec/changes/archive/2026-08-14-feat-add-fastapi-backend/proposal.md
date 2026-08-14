## Why

The snekdo CLI only supports local, interactive use. Adding a FastAPI backend exposes the same todo CRUD operations over a REST API, enabling programmatic access, web integrations, and remote clients without changing the existing CLI behavior.

## What Changes

- Add a new `snekdo/api.py` module that wires the existing `Todo` model and `TodoStorage` into a FastAPI application.
- Expose REST endpoints for listing, showing, adding, completing, modifying, and deleting todos.
- Add a `serve` subcommand to the CLI (`snekdo serve`) that starts the FastAPI server with uvicorn.
- Add a health-check endpoint (`/api/v1/health`) and an OpenAPI schema endpoint (`/api/v1/openapi.json`).
- Add pytest tests for the API endpoints.
- Add `fastapi` and `uvicorn` as project dependencies (optional `[api]` extra).

## Capabilities

### New Capabilities

- `fastapi-backend`: REST API surface over the existing todo storage, served via FastAPI/uvicorn.

### Modified Capabilities

<!-- No existing capability requirements change; the CLI and storage behavior remain unchanged. -->

## Impact

- **New dependencies**: `fastapi`, `uvicorn` (added to `dependencies` or `[project.optional-dependencies]`).
- **New files**: `snekdo/api.py`, `tests/test_api.py`.
- **Modified files**: `snekdo/__main__.py` (new `serve` subcommand), `pyproject.toml` (new dependencies).
- **No breaking changes** to existing CLI or storage behavior.
