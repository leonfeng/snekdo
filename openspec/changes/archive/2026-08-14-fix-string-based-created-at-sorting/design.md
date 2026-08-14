## Context

The `created_at` field on `Todo` is stored as an ISO 8601 string (e.g., `2024-01-01T00:00:00`). In `snekdo/__main__.py`, the `handle_list` function sorts by this field using `key=lambda x: x.created_at`, which performs lexicographic string comparison. While ISO 8601 strings sort correctly when the format is perfectly consistent, this approach is fragile and semantically incorrect.

## Goals / Non-Goals

**Goals:**
- Convert `created_at` strings to `datetime` objects when sorting by created date.
- Preserve existing default sort order (newest first) and reverse behavior.
- Handle empty/missing `created_at` values gracefully.

**Non-Goals:**
- Change the storage format of `created_at` (remains an ISO 8601 string).
- Modify sorting for other fields (title, priority, completed).
- Add new CLI flags or change existing ones.

## Decisions

### Decision: Use `datetime.fromisoformat()` for parsing

Use Python's `datetime.fromisoformat()` to parse the stored string. This handles standard ISO 8601 formats including timezone offsets (Python 3.11+).

**Rationale**: It is the standard library function designed for this purpose, requires no new dependencies, and correctly handles varying precision.

**Alternatives considered**:
- `datetime.strptime()` with a fixed format — less flexible, would fail on timezone-aware or microsecond formats.
- Store `created_at` as a `datetime` object in the model — requires database migration and changes to `models.py`, more invasive.

### Decision: Treat empty `created_at` as epoch (earliest)

When `created_at` is empty, use `datetime.min` (epoch) as the sort key so empty values sort consistently.

**Rationale**: Empty values are rare (only from pre-v0.1 data or manual edits). Treating them as earliest is a reasonable, deterministic choice.

### Decision: Compute sort key lazily in `handle_list`

Only parse `created_at` when sorting by `created_at`, to avoid unnecessary parsing overhead for other sort fields.

## Risks / Trade-offs

- **Risk**: Existing data with malformed `created_at` strings will raise `ValueError`.
  **Mitigation**: Wrap parsing in a try/except and fall back to string comparison or treat as epoch.
- **Risk**: Performance impact from parsing on every list operation.
  **Mitigation**: Minimal — parsing a single ISO 8601 string is fast, and list operations are infrequent.

## Migration Plan

No migration needed. The change is purely in the sorting logic and is backward-compatible.

## Open Questions

None.
