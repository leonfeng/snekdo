## Context

The snekdo project has a CLI, a FastAPI server, and a sync mechanism. The `ServerHttpClient.update_todo()` method already accepts a `completed` parameter and sends it to the server when provided. However, the `_sync()` function in `snekdo/__main__.py` never passes `completed` when updating existing todos during push/both sync. This means the completion status is never synchronized between the local storage and the server.

## Goals

- Ensure the sync command synchronizes the `completed` field between local storage and the server.
- Add tests to verify the fix.

## Non-Goals

- Do not change the `completed` field handling in the API client's `update_todo` method itself (it already works correctly).
- Do not modify the `TodoUpdate` Pydantic model or the `modify_todo` endpoint.
- Do not change the pull direction's handling of other fields.

## Decisions

1. **Fix location**: The fix is in `_sync()` in `snekdo/__main__.py`, where the `update_todo` call is missing the `completed` argument.
2. **Approach**: Pass the local todo's `completed` value to `client.update_todo()` when updating existing todos during push/both sync.
3. **Testing**: Add/update tests in `tests/test_cli.py` to verify the `completed` field is included in sync operations.
4. **Spec**: Create a new spec `api-client-completed-sync` and update the `cli-sync` spec to reflect the new behavior.