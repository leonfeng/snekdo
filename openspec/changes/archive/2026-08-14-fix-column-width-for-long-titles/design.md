## Context

The `list` command in `snekdo/__main__.py` prints a fixed-width table using Python format specs like `{title:<30}`. This silently truncates any title longer than 30 characters. The existing `list-display` spec does not cover this behavior.

## Goals / Non-Goals

**Goals:**
- Compute the Title column width dynamically from the actual titles in the current list.
- Display the full title when it fits; truncate with `...` only when the title exceeds a reasonable maximum width.
- Keep all columns aligned.

**Non-Goals:**
- Do not change other column widths (ID, Status, Priority, Due, Created At) — keep them fixed.
- Do not change the `show` command or other commands.
- Do not add wrapping to multiple lines; truncation with ellipsis is sufficient.

## Decisions

1. **Dynamic Title width**: Compute the width of the longest title (capped at a maximum, e.g., 40 characters) and use it for both the header and all rows. This ensures full titles are visible.
2. **Ellipsis truncation**: When a title is longer than the maximum width, truncate to `max_title_width - 3` characters and append `...`.
3. **Fixed other columns**: Keep ID (35), Status (10), Priority (10), Due (15), Created At (25) at their current widths.
4. **Total line width**: With the dynamic Title column, the total line may exceed 125 characters. This is acceptable for a terminal todo list.

## Risks / Trade-offs

- **Risk**: Long titles may make the table very wide on small terminals. **Mitigation**: Cap the Title column at a maximum width (40 chars) so the table never becomes excessively wide.
- **Risk**: Existing tests may assert the exact output line length of 125. **Mitigation**: Tests will need updating; the design documents the new expected behavior.

## Migration Plan

No migration needed. The change is purely in the display formatting of the `list` command.

## Open Questions

None.
