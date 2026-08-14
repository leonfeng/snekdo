## Context

The `list` command in `snekdo/__main__.py` prints a fixed-width table. Some columns use dynamic widths (ID, Title) while others use fixed widths (Status: 10, Priority: 10, Due: 15, Created At: 25). The separator between columns is a single space, but the visual whitespace appears inconsistent because fixed-width columns leave large gaps when their content is short, while dynamic columns are only as wide as their content.

## Goals / Non-Goals

**Goals:**
- Make the whitespace between columns uniform by computing all column widths from content where possible and using consistent single-space separators.
- Keep the table aligned and readable.
- Preserve existing behavior for truncation and sorting.

**Non-Goals:**
- Do not change the `show` command or other commands.
- Do not add multi-line wrapping.
- Do not change the storage format or CLI arguments.

## Decisions

1. **Uniform separator**: Use a single space between all columns. This is already the case; the fix ensures that column widths are computed consistently so the visual spacing is uniform.

2. **Dynamic column widths**: Continue computing ID and Title column widths from content (capped at maximums of 35 and 40 respectively).

3. **Fixed column widths**: Keep the fixed widths for Status (10), Priority (10), Due (15), and Created At (25) columns, but ensure they are padded consistently. The "uniform whitespace" is achieved by ensuring all columns use the same separator (single space) and are padded to their allocated width.

4. **Total line width**: With dynamic columns, the total line may exceed the previous fixed width of 125 characters. This is acceptable.

## Risks / Trade-offs

- **Risk**: Long titles or IDs may make the table very wide on small terminals. **Mitigation**: Cap the dynamic columns at maximum widths (Title: 40, ID: 35).
- **Risk**: Existing tests may assert exact output line lengths. **Mitigation**: Update tests to reflect the new formatting.

## Migration Plan

No migration needed. The change is purely in the display formatting of the `list` command.

## Open Questions

None.
