## Why

The `GET /api/v1/todos` endpoint defaults the `status` query parameter to `None`,
which means it returns **all** todos (pending + completed). This is inconsistent
with the CLI `list` command, which defaults to filtering by `pending` status.
Users expect the API to match the CLI's default behavior.

## What Changes

- Change the `status` parameter in `list_todos` from `Query(default=None, ...)` to
  `Query(default="pending", ...)`.
- Update the `fastapi-backend` OpenSpec capability to reflect the pending-default
  behavior and add a scenario covering it.

## Capabilities

### Modified Capabilities

- `fastapi-backend`: Add a requirement "List todos defaults to pending" and a
  scenario verifying that completed todos are excluded by default.

## Impact

- **Affected code**: `snekdo/api.py` (`list_todos` signature).
- **No new dependencies**.
- **Compatibility**: The API now returns fewer results by default. Clients that
  need all todos can pass `?status=all`.
