## Context

The `snekdo` application has two registration entry points:
- API: `snekdo/api_auth.py` `register()` — sets `created_at=datetime.now().isoformat()`.
- Web: `snekdo/web_auth.py` `register_submit()` — does **not** set `created_at`, leaving it as an empty string.

Both entry points create a `User` dataclass and persist it via `UserStorage.add()`. The `User` model's `created_at` field defaults to `""`.

## Goals / Non-Goals

**Goals:**
- Make web registration set `created_at` to the current ISO 8601 timestamp, consistent with the API registration endpoint.
- Add a test that verifies web-registered users have a non-empty `created_at`.

**Non-Goals:**
- No changes to the `User` dataclass, storage format, or API contract.
- No migration of existing users (existing empty `created_at` values are a data quality issue, but this change only affects new registrations).

## Decisions

**Decision: Set `created_at` at the point of `User` creation in `register_submit`.**

Rationale: The API endpoint already sets `created_at=datetime.now().isoformat()` at the point of `User` creation. The web handler should follow the same pattern. This keeps the timestamp assignment co-located with the `User` construction, making it easy to find and consistent across entry points.

Alternative considered: Set `created_at` in `User.__post_init__` so it is always populated. However, this would change the semantics of the `User` model for all callers, including tests that create `User` objects without a timestamp. The narrower fix is to set it only in the registration handler.

## Risks / Trade-offs

- **Risk**: Existing tests that register via the web form may now assert on `created_at`.
  **Mitigation**: Update the web test to verify `created_at` is non-empty.

## Migration Plan

No migration needed. The change only affects new web registrations. Existing stored users are unaffected.

## Open Questions

None.
