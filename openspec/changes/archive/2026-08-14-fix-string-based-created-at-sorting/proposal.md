## Why

The `created_at` field is stored as an ISO 8601 string and the list command sorts by string comparison (`key=lambda x: x.created_at`). This is fragile and semantically incorrect: string ordering breaks with mixed formats, timezone-aware values, or any format change, and it treats a date as opaque text rather than a temporal value.

## What Changes

- Modify `handle_list` in `snekdo/__main__.py` so that sorting by `created_at` converts the stored string to a `datetime` object before comparison.
- Preserve existing behavior for all other sort fields (title, priority, completed).
- Handle missing/empty `created_at` values gracefully (treat as epoch / earliest).
- Add/update tests to verify correct chronological ordering.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `todo-sorting`: The "Sort by created date" requirement is modified to require proper datetime-based comparison instead of string-based comparison.

## Impact

- Affected code: `snekdo/__main__.py` (`handle_list`), `tests/test_cli.py` (sort tests).
- No new dependencies.
- No API or CLI interface changes.
- Backward-compatible: output ordering improves only where string comparison previously produced wrong results.
