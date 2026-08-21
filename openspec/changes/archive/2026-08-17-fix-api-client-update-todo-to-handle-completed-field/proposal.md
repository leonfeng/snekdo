## Why

The `snekdo sync` command pushes local todos to the server via `ServerHttpClient.update_todo()`, but it never passes the `completed` field. As a result, when a user marks a todo complete locally and syncs, the server still shows the todo as incomplete (and vice versa). The API client's `update_todo` method already accepts a `completed` parameter, but the sync path never uses it, so the completion status is never synchronized.

## What Changes

- Update `_sync()` in `snekdo/__main__.py` to pass the local todo's `completed` value when calling `client.update_todo()` during push/both sync.
- Add an explicit `completed` argument to the `update_todo` call site in the push/update loop.
- Add/update tests to verify that the `completed` field is included in `update_todo` calls during sync and that the server response reflects the correct completion status.

## Capabilities

### New Capabilities

- `api-client-completed-sync`: Ensure the API client's `update_todo` method and the sync function properly handle the `completed` field when synchronizing todos, so completion status is consistent between local storage and the server.

### Modified Capabilities

- `cli-sync`: Update the sync push/update behavior to include the `completed` field when updating existing todos on the server.

## Impact

- Affected code: `snekdo/__main__.py` (`_sync`), `snekdo/api_client.py` (`update_todo`), `tests/test_cli.py` (sync tests).
- No API-level breaking changes; the server already supports `completed` in `PUT /api/v1/todos/{id}`.
- Existing sync tests will need to be updated to assert the `completed` argument.