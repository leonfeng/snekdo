## Context

See proposal for motivation. The `Todo` dataclass lives in `snekdo/models.py`; JSON persistence is in `snekdo/storage.py`, SQLite in `snekdo/storage_sqlite.py`. Existing optional fields (`user_id`, `repeat`, `last_completed_at`) show the established pattern for adding fields with backward-compatible defaults.

## Goals / Non-Goals

**Goals:**
- Add `tags` and `category` fields to `Todo` with correct defaults.
- Ensure serialization round-trips both fields.
- Ensure old JSON files (without the keys) load without error.

**Non-Goals:**
- No storage, CLI, API, or web changes in this slice (handled by later changes).

## Decisions

1. **`tags` is `list[str]` with default `[]`.** Matches the many-to-many nature of tags; empty list is the natural absence value (unlike `category` where `None` expresses "no category").
2. **`category` is `str | None` with default `None`.** A todo belongs to at most one category.
3. **`from_dict` uses `data.get("tags", [])` and `data.get("category") or None`.** The `or None` pattern matches existing treatment of `user_id`/`due` so empty strings normalize to `None`.
4. **No migration for JSON storage needed.** Missing keys simply resolve to defaults.

## Risks / Trade-offs

- [Existing JSON files lack the keys] → `from_dict` defaults handle this; tested explicitly.
- [Mutable default `[]` in dataclass] → Use `field(default_factory=list)` to avoid the shared-mutable-default pitfall.

## Migration Plan

None required for this slice. Old files load with defaults.
