## Context

`Todo.from_dict()` in `snekdo/models.py` deserializes JSON-stored dicts into `Todo` objects. The `due` field is already normalized (`data.get("due") or None`), but `user_id` is not (`data.get("user_id")`), so stored `user_id: ""` values produce `Todo` objects with `user_id == ""` instead of `None`. This breaks the web UI's user-filtering logic, which treats `None` and `""` as "no user" but only consistently when both are `None`.

## Goals / Non-Goals

**Goals:**
- Normalize empty strings to `None` for nullable `Todo` fields (`due` and `user_id`) in `Todo.from_dict()`.
- Ensure consistent behavior when loading todos from JSON storage (both CLI sync and API).
- Add/update tests to cover the normalization.

**Non-Goals:**
- Changing `to_dict()` serialization (already includes all fields).
- Changing the `User` model (all fields are non-nullable strings).
- Adding new dependencies or changing the data file format.

## Decisions

### Decision: Use `or None` for nullable string fields

Use the pattern `data.get("field") or None` for `due` and `user_id` in `from_dict()`. This is consistent with the existing `due` handling and clearly converts any falsy value (empty string) to `None`.

**Alternatives considered:**
- `data.get("field", "") or None` — equivalent but more verbose.
- `None if data.get("field") == "" else data.get("field")` — more explicit but longer.
- `data.get("field")` with a default of `None` — doesn't handle empty strings.

The `or None` pattern is chosen for simplicity and consistency with the existing `due` handling.

### Decision: Only modify `from_dict()`, not storage or API

The root cause is in the model's deserialization. Storage and API already work with whatever `Todo` objects they receive. Fixing `from_dict()` ensures all callers (storage, CLI sync, API) get normalized objects.

## Risks / Trade-offs

- **Risk**: Existing JSON data with `user_id: ""` will now load as `None` instead of `""`. This is the intended behavior, but any code that explicitly checks `todo.user_id == ""` will break.
  **Mitigation**: Search the codebase for `== ""` checks on `user_id` and update them to `is None`.
- **Risk**: The change affects all `from_dict()` callers (storage load, sync).
  **Mitigation**: Tests cover both `due` and `user_id` normalization.

## Migration Plan

No migration is needed. The fix is applied at deserialization time. Existing JSON files with `user_id: ""` will load correctly as `None`.

## Open Questions

None.
