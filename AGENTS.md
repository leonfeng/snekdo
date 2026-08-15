# AGENTS.md

snekdo — a Python CLI todo list manager (single package `snekdo/`, tests in `tests/`).

## Entry points
- CLI: `snekdo.__main__:main` → `create_parser()` builds subcommands `add|list|complete|delete|modify|show|serve|sync`.
- API: `snekdo.api:create_app(storage_path=...)` → FastAPI at `/api/v1/*`.
- Package: `snekdo/__init__.py`, `snekdo/__main__.py`, `snekdo/models.py`, `snekdo/storage.py`, `snekdo/api.py`, `snekdo/api_client.py`.

## Storage
- Default path: `~/.snekdo/todos.json`. Override with `--storage <path>` on every subcommand.
- JSON file, file locking via `fcntl` on Linux and a `fake_fcntl` fallback (see `snekdo/storage.py`).

## Key wiring facts (easy to get wrong)
- `--storage` is accepted on **every** subcommand; the top-level `--storage` is also parsed. `_get_storage_path(args)` resolves it.
- `TodoStorage(storage_path=...)` is the shared abstraction used by both CLI and API.
- Due dates are validated with `validate_due_date()` (CLI) / `_validate_due_date()` (API): `YYYY-MM-DD`, must not be in the past.
- List sort fields: `created_at|title|priority|completed`. `created_at` is parsed via `_parse_created_at()` (ISO 8601, `datetime.min` for empty).
- Priority sort order: high(0) < medium(1) < low(2).
- List display: dynamic Title/ID column widths (capped 40/35), fixed widths for Status/Priority/Due/Created At, single-space separators, titles truncated with `...`.
- `handle_list` filters by status (`pending` default), priority, then sorts, then limits.
- `modify` only updates fields present in kwargs; empty string is a valid value (clears field).

## API
- Endpoints: `GET /api/v1/health`, `GET /api/v1/todos`, `GET /api/v1/todos/{id}`, `POST /api/v1/todos`, `POST /api/v1/todos/{id}/complete`, `PUT /api/v1/todos/{id}`, `DELETE /api/v1/todos/{id}`.
- Pydantic models: `TodoCreate`, `TodoUpdate`, `TodoResponse`, `HealthResponse`, `MessageResponse`.
- `TodoResponse.from_todo()` maps `Todo` → response.
- OpenAPI docs at `/docs`, schema at `/openapi.json`.

## Sync
- `snekdo sync --server <url> --direction pull|push|both` synchronizes local JSON with the FastAPI server via `ServerHttpClient` (uses `urllib.request`, no extra deps).
- `pull`: server is source of truth. `push`: local wins for existing, creates missing, deletes absent-on-local (only push/both).

## Running
- Install: `pip install -e .` (CLI) or `pip install -e ".[api]"` (server). Tests: `pip install -e ".[test]"`.
- Run tests: `pytest` (testpaths = tests, pythonpath = .).
- Run CLI: `python -m snekdo --help` or `snekdo --help`.
- Run server: `snekdo serve` (default 127.0.0.1:8000).

## OpenSpec
- `openspec/` holds `config.yaml`, `specs/` (main specs) and `changes/` (delta changes). The workflow is `spec-driven`.
- Commands: `/opsx-apply`, `/opsx-archive`, `/opsx-explore`, `/opsx-propose`, `/opsx-sync`, `/opsx-update`.

## Gotchas
- `storage_path` is passed as a string to `create_app()` and `TodoStorage()`; `_get_storage_path()` returns a `Path`.
- `handle_serve` imports `uvicorn` lazily; fails gracefully if missing.
- `ServerHttpClient._request` treats any non-2xx as `ServerError`; connection failures become `ConnectionError`.
- `fake_fcntl` is used only when `fcntl` is unavailable (e.g., Windows); on Linux real `fcntl.flock` is used.
- `Todo.__post_init__` generates a nanoid ID if `id` is empty; `from_dict` preserves the stored ID.
- `created_at` is stored as an ISO 8601 string; empty/missing parses to `datetime.min`.
