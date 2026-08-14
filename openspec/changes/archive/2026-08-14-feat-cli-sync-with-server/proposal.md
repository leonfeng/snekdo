## Why

The snekdo CLI currently operates only against a local JSON storage file, while the FastAPI backend (`snekdo serve`) exposes the same data over HTTP. There is no way to synchronize the CLI with a running server, so users cannot pull server-side changes into the CLI or push local changes to the server. This feature adds a `snekdo sync` command that bridges the CLI and the server.

## What Changes

- Add a new `sync` subcommand to the CLI that communicates with the FastAPI server.
- The `sync` command supports:
  - Pulling all todos from the server into the local storage (overwriting local with server state).
  - Pushing local todos to the server (creating new todos on the server).
  - Resolving conflicts when a todo exists on both the local storage and the server with diverging state.
- Add a `--server` flag to specify the server base URL (default `http://127.0.0.1:8000`).
- Add a `--direction` flag to control sync direction: `pull`, `push`, or `both`.
- Add an HTTP client helper in `snekdo/api_client.py` for making requests to the server.
- Add tests for the sync command and HTTP client.

## Capabilities

### New Capabilities

- `cli-sync`: Synchronize CLI local storage with the FastAPI server via a new `snekdo sync` command.

### Modified Capabilities

- `fastapi-backend`: Adds a new `--server`/`--direction` usage pattern that the server must tolerate (no behavior change on the server itself; the server already supports all CRUD operations the sync command needs).

## Impact

- Affected code: `snekdo/__main__.py` (new `sync` subcommand and handler), `snekdo/api.py` (new HTTP client helpers), `snekdo/storage.py` (no changes), `tests/test_cli.py` (new tests), `tests/test_api.py` (new HTTP client tests).
- No new dependencies required; the HTTP client uses the standard library `urllib` or the existing `requests`-free approach.
- The `pyproject.toml` does not need changes since we use only the standard library for HTTP.
