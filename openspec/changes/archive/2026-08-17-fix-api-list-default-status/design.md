## Context

`list_todos` in `snekdo/api.py` uses `status: str | None = Query(default=None, ...)`.
The CLI's `handle_list` uses `pending` as the default filter. The API should match.

## Goals / Non-Goals

**Goals:**
- Default the API `status` query to `"pending"` so `GET /api/v1/todos` returns only
  pending todos, matching the CLI.
- Update the OpenSpec `fastapi-backend` capability to document this behavior.

**Non-Goals:**
- No changes to the CLI (it already defaults to pending).
- No changes to the `Todo` model, storage, or other endpoints.

## Decisions

- **Decision**: Use `Query(default="pending", enum=["all", "pending", "completed"])`.
  - **Rationale**: Matches the CLI default and the existing enum; minimal change.
  - **Alternative**: A separate `default_status` config. Rejected as unnecessary.

## Risks / Trade-offs

- **Risk**: Clients expecting all todos by default will now get only pending.
  - **Mitigation**: They can pass `?status=all` to get all todos. This is the
    intended behavior matching the CLI.

## Migration Plan

No migration needed. The API change is backward-compatible for clients that
explicitly pass `?status=`; clients relying on the (incorrect) all-todos default
must add `?status=all`.

## Open Questions

None.
