## Context

The FastAPI app (`snekdo/api.py`) already authenticates every todo endpoint via
JWT and resolves the authenticated user. The `TodoStorage` layer
(`snekdo/storage.py`) supports per-user filtering through the `user_id`
argument on `load`, `get`, `delete`, `complete`, and `modify`. The bug is that
`complete_todo`, `modify_todo`, and `delete_todo` only pass `user_id` to the
initial `storage.get()` guard but omit it on the mutating call.

## Goals / Non-Goals

**Goals:**
- Ensure complete, modify, and delete storage calls are scoped to the
  authenticated user's ID, matching the existing guard checks.
- Add test coverage (via the spec) for cross-user mutation prevention.

**Non-Goals:**
- No changes to the storage layer (it already supports `user_id`).
- No changes to authentication, JWT handling, or the CLI.
- No changes to the web frontend.

## Decisions

- **Approach**: Pass `user_id=current_user.id` as a keyword argument to the
  mutating `storage` calls. This is the minimal, safest change and reuses the
  existing `user_id` parameter that `load()` already filters on.
- **Alternative considered**: Add a wrapper that always injects `user_id`.
  Rejected — unnecessary abstraction for a three-call fix.
- **Return value handling**: `storage.modify()` and `storage.delete()` return
  `bool`. The current code ignores the return value and instead calls
  `storage.get()` afterward to refresh the object. For `modify_todo`, the
  follow-up `storage.get()` is also scoped to `user_id` after the fix. For
  `delete_todo`, the response only echoes the title from the pre-check `todo`
  object, which is already authorized, so no additional get is needed.

## Risks / Trade-offs

- **Risk**: Existing tests that create a todo and immediately delete/modify it
  with the same user should continue to pass (they already use the same user).
- **Risk**: If a todo has `user_id=None` (legacy data), the filter
  `t.user_id == user_id` will never match, so the mutation will silently
  become a no-op (return 404). This is consistent with the existing guard
  behavior and the `load()` filter.
- **Mitigation**: Add explicit cross-user tests to verify the 404 behavior.

## Migration Plan

This is a bug fix with no API contract change. Deploy as-is; no data
migration or feature flag needed.

## Open Questions

None. The fix is deterministic and fully covered by the spec scenarios.
