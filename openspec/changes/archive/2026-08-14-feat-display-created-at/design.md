## Context

The `list` command in `snekdo/__main__.py` currently renders a table with columns: ID, Title, Status, Priority, Due. The `Todo` model already stores `created_at` as an ISO 8601 string, but the list view does not display it.

## Goals / Non-Goals

**Goals:**
- Add a `Created At` column to the list output table
- Display the `created_at` value for each todo row
- Maintain the existing table layout and alignment
- Add tests covering the new column

**Non-Goals:**
- No changes to the data model or storage format
- No new CLI flags for the list command
- No changes to sorting, filtering, or limiting behavior
- No formatting of the date (keep raw ISO 8601 string)

## Decisions

### Decision: Add column to existing table

**Choice**: Append a `Created At` column to the existing header/row print in `handle_list()`.

**Rationale**: 
- Minimal change to existing code
- The `created_at` field already exists on the `Todo` model
- No new formatting logic needed
- Consistent with the existing table-based output approach

**Alternatives considered**:
- Reformat the entire output to a different layout (e.g., one todo per line) - more disruptive
- Use `datetime` parsing for display - adds complexity and is unnecessary since the stored value is already ISO 8601

### Decision: Column width

**Choice**: Use `<35` for the Created At column, matching the existing column widths.

**Rationale**: ISO 8601 strings are typically 19-24 characters, so 35 characters is sufficient.

## Risks / Trade-offs

### Risk: Table width exceeds terminal

**Impact**: Low - the table already has 5 columns; adding a 6th may cause wrapping on small terminals.

**Mitigation**: The existing 5-column table already requires wide terminals; this is consistent with the current UX.

### Risk: Existing tests may fail due to output format change

**Impact**: Medium - tests that assert exact output strings will need updating.

**Mitigation**: Update existing test assertions to include the new column.

## Migration Plan

This is a pure output format change. No data migration is required since `created_at` is already stored.

## Open Questions

None - the implementation approach is clear.
