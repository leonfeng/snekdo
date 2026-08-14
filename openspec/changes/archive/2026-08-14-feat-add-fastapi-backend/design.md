## Context

The existing snekdo application is a CLI-only todo manager built on argparse, the standard library, and a JSON file storage layer (`snekdo/storage.py`). The `Todo` model (`snekdo/models.py`) and `TodoStorage` class already implement the core business logic. We need to expose the same operations over HTTP without refactoring the CLI.

## Goals / Non-Goals

**Goals:**
- Add a FastAPI-based REST API that reuses `Todo` and `TodoStorage`.
- Provide a `serve` CLI subcommand that launches the API server with uvicorn.
- Keep the existing CLI behavior untouched.
- Make the API testable with pytest (using `TestClient`).

**Non-Goals:**
- No database migration or new data model.
- No authentication or rate limiting.
- No WebSocket or real-time features.
- No changes to the CLI commands (`add`, `list`, `show`, etc.).

## Decisions

### Decision: Reuse existing storage and model
- **Rationale**: The `Todo` dataclass and `TodoStorage` class already implement persistence, locking, and CRUD. The API should delegate to them rather than reimplementing logic.
- **Alternative considered**: Extracting a shared service layer. This is unnecessary because `TodoStorage` is already a clean abstraction.

### Decision: Use Pydantic request/response models
- **Rationale**: FastAPI integrates with Pydantic for validation and serialization. We will define simple Pydantic models (`TodoCreate`, `TodoUpdate`, `TodoResponse`) that wrap the `Todo` dataclass.
- **Alternative considered**: Using the `Todo` dataclass directly. This would lose request validation and OpenAPI schema generation.

### Decision: Single FastAPI app instance
- **Rationale**: A single `app` instance in `snekdo/api.py` follows the standard FastAPI pattern and keeps the code simple.
- **Alternative considered**: Using FastAPI routers with a separate `main.py`. This adds unnecessary complexity for a small project.

### Decision: Dependency injection for storage
- **Rationale**: FastAPI's `Depends()` allows the storage instance to be injected into endpoints, making it easy to test with a mock or in-memory storage.
- **Alternative considered**: Global singleton. This is harder to test and less idiomatic in FastAPI.

### Decision: Default server host/port
- **Rationale**: uvicorn defaults to `127.0.0.1:8000`, which is the standard FastAPI development default. We expose `--host` and `--port` CLI flags to override it.

### Decision: Dependencies as optional extras
- **Rationale**: `fastapi` and `uvicorn` are not needed for CLI-only usage. We add them under `[project.optional-dependencies]` with an `api` extra, and also include them in `dependencies` for the `serve` command to work.

## Risks / Trade-offs

- **Risk**: Adding `fastapi` and `uvicorn` increases the dependency footprint.
  - **Mitigation**: Make them optional extras; CLI-only users are unaffected.
- **Risk**: uvicorn may not be available on all systems.
  - **Mitigation**: Provide a clear error message if uvicorn is missing when `serve` is invoked.
- **Risk**: File locking conflicts between CLI and API concurrent access.
  - **Mitigation**: Both use the same `TodoStorage` with `fcntl` locking; concurrent writes are serialized.

## Migration Plan

- No data migration required; the JSON storage format is unchanged.
- Existing CLI users continue to use `snekdo add`, `snekdo list`, etc.
- New users can start the API with `snekdo serve`.

## Open Questions

- Should the API use a version prefix (`/api/v1/`)? Yes, for future extensibility.
- Should the `serve` command support hot reloading? Not in this change; uvicorn's `--reload` can be used separately.
- Should we add an HTML admin interface? Not in this change; focus on JSON API.
