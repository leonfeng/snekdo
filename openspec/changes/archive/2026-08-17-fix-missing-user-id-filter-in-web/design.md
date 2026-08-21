## Context

The snekdo project has a CLI, a FastAPI REST API, and a Jinja2/HTMX web frontend. Todos are stored in a single JSON file (`~/.snekdo/todos.json`). The `Todo` model has a `user_id` field for per-user isolation, but the `to_dict()` serialization conditionally omits it when `None`. The CLI `add` command does not set `user_id`, while the API and web frontend do set it. This inconsistency causes CLI-created todos to be invisible in the web UI.

## Goals / Non-Goals

**Goals:**
- Ensure `Todo.to_dict()` always serializes the `user_id` field so the stored JSON is consistent.
- Ensure the CLI `add` command sets `user_id` on created todos.
- Ensure the web list endpoints filter by the authenticated user's `user_id`.
- Add tests covering cross-interface visibility (CLI-created todos visible in web, and vice versa).

**Non-Goals:**
- No changes to the JWT/token authentication mechanism.
- No changes to the API contract (no new endpoints or response fields required).
- No changes to the storage file format beyond adding a consistent `user_id` key.

## Decisions

1. **Always serialize `user_id` in `Todo.to_dict()`**: Instead of conditionally including `user_id` only when it's not `None`, we always include it. This ensures the JSON file always has a `user_id` key for every todo, making the data model consistent and predictable. The `from_dict()` method already handles `None` correctly.

2. **Set `user_id` in CLI `add`**: The CLI `handle_add` function will set `user_id` on created todos. Since the CLI doesn't have a logged-in user in the current implementation, we leave it as `None` for backward compatibility but ensure the field is present in the serialized output. Actually, since the CLI doesn't authenticate users, we keep `user_id=None` for CLI-created todos but ensure the field is serialized.

3. **Web list filtering**: The web list endpoints already filter by `user_id` from the authenticated session. No changes needed here; we just ensure the data is consistent.

4. **No API changes**: The API already filters by `current_user.id`. No changes needed.

## Risks / Trade-offs

- **Risk**: Existing todos in the JSON file don't have a `user_id` key. After this change, `from_dict()` will return `None` for `user_id`, and the web UI will filter them out for authenticated users. This is expected behavior — these todos belong to no one.
- **Risk**: The CLI doesn't authenticate users, so CLI-created todos will have `user_id=None`. These todos won't appear in the web UI for authenticated users. This is a known limitation — the CLI and web UI have different authentication models.
- **Mitigation**: The `from_dict()` method already handles missing `user_id` by defaulting to `None`, so no migration is needed for existing data.

## Migration Plan

No migration is needed. The `from_dict()` method already handles missing `user_id` by defaulting to `None`. New todos will always have the `user_id` key in the JSON.

## Open Questions

- Should the CLI also authenticate users and set `user_id` on created todos? This is beyond the scope of this change.
- Should the web UI display a `user_id` column? This is not required for the fix.