## Context

The snekdo project has a CLI (`snekdo/__main__.py`) and a FastAPI backend (`snekdo/api.py`) that both operate on the same `TodoStorage` model. The CLI uses `TodoStorage` to read/write a local JSON file, while the server exposes the same operations via HTTP endpoints. There is no mechanism for the CLI to communicate with the server to synchronize data.

## Goals / Non-Goals

**Goals:**
- Add a `snekdo sync` CLI subcommand that communicates with the FastAPI server.
- Support three sync directions: `pull` (server → local), `push` (local → server), and `both`.
- Implement conflict resolution: server wins on pull/both, local wins on push.
- Use only the Python standard library (`urllib.request`) for HTTP to avoid new dependencies.

**Non-Goals:**
- Do not modify the existing `serve` command or the FastAPI endpoints.
- Do not add authentication or authorization to the sync command.
- Do not implement incremental sync (sync will be a full resync of all todos).
- Do not add a `--server` flag to commands other than `sync`.

## Decisions

### Decision 1: Use `urllib.request` for HTTP
- **Rationale**: The project already depends on `fastapi` and `uvicorn`, but the sync command should not introduce a new dependency like `requests`. Using `urllib.request` from the standard library keeps the dependency footprint minimal.
- **Alternative**: Use `requests`. Rejected because it would require adding a new dependency to `pyproject.toml`.

### Decision 2: Server wins on pull/both
- **Rationale**: When pulling from the server, the server is the source of truth. This is the most common use case (e.g., the server was updated by another client, and the CLI needs to catch up).
- **Alternative**: Last-write-wins based on `created_at`. Rejected because it adds complexity and the server is the authoritative source.

### Decision 3: Local wins on push
- **Rationale**: When pushing to the server, the local CLI is the source of truth. The user is explicitly choosing to push their local state.
- **Alternative**: Server wins on push too. Rejected because it would silently overwrite local changes.

### Decision 4: Default server URL
- **Rationale**: The server defaults to `http://127.0.0.1:8000` (matching the `serve` command's defaults), so the sync command uses the same default.
- **Alternative**: Read from a config file. Rejected because it adds complexity; the `--server` flag is sufficient.

### Decision 5: Full resync
- **Rationale**: A full resync is simpler to implement and test. Incremental sync can be added later.
- **Alternative**: Incremental sync based on `created_at`. Rejected because it adds complexity and is not required by the spec.

## Risks / Trade-offs

- **Risk**: The `urllib.request` approach does not support HTTP/2, but HTTP/1.1 is sufficient for this use case.
- **Risk**: If the server and local storage have different storage paths, the sync may not work correctly. Mitigation: the `--storage` flag ensures the local path is explicit.
- **Risk**: Large todo lists may cause slow syncs. Mitigation: the API already supports `limit` and pagination can be added later.
- **Trade-off**: Full resync on every `sync` is simpler but less efficient than incremental sync.

## Migration Plan

- No migration needed. This is a new feature that does not change existing behavior.
- The `snekdo sync` command is additive and does not affect existing commands.

## Open Questions

- None. The scope is well-defined by the spec.
