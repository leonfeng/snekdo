## Context

The `handle_list` function in `snekdo/__main__.py` builds a table with a fixed 35-character ID column and a dynamic Title column. The Title column width is already computed from the longest title (capped at 40). The ID column uses a hardcoded width that doesn't match the actual nanoid ID length (~21 chars).

## Goals / Non-Goals

**Goals:**
- Compute the ID column width dynamically from the longest ID in the current list, capped at a reasonable maximum.
- Apply the same truncation-with-ellipsis behavior to IDs that exceed the maximum width, consistent with the Title column.
- Keep the table header and data rows aligned.

**Non-Goals:**
- Changing the order of columns.
- Changing the storage format or ID generation.
- Adding new commands or modifying existing behavior beyond the list display.

## Decisions

1. **Dynamic ID column width**: Compute `id_width` as `min(max(len(t.id) for t in todos), max_id_width)` and ensure it is at least `len("ID")`. This mirrors the existing Title column width computation.

2. **Max ID width cap**: Use a cap of 35 characters (the current hardcoded value) to prevent extremely long IDs from making the table too wide. This is a reasonable default that matches the current output width.

3. **ID truncation**: Apply the same `_truncate_title` function (renamed/reused for IDs) to truncate IDs that exceed the max width with an ellipsis.

4. **Update test helper**: The `_parse_list_line` function in `tests/test_cli.py` currently assumes a fixed 35-character ID column. It will be updated to parse the dynamic ID width by finding the first space after the ID column.

## Risks / Trade-offs

- **Risk**: Tests that assert exact output strings may fail because the spacing changes. **Mitigation**: Update affected tests to use the dynamic parsing approach.
- **Risk**: Very short IDs (e.g., 5 chars) will make the ID column narrower, which is the intended behavior. **Mitigation**: Ensure the column is at least as wide as the "ID" header.
- **Risk**: IDs with special characters. **Mitigation**: IDs are nanoid strings (alphanumeric + underscore + hyphen), so no special handling needed.

## Migration Plan

No migration needed. This is a display-only change that improves the existing list output.

## Open Questions

None. The approach is straightforward: compute ID width dynamically and apply truncation.
