## Context

The CLI currently represents pending status as a single space character (`" "`) in both the list table and the show detail view. Completed status uses a checkmark (`"✓"`). This asymmetry makes pending items hard to identify at a glance.

## Goals / Non-Goals

**Goals:**
- Display the literal text "pending" for todos that are not completed, in both the list and show commands.
- Keep the checkmark ("✓") for completed todos.

**Non-Goals:**
- No changes to sorting, filtering, or other display columns.
- No changes to the data model or storage format.
- No changes to the `--status` filter behavior (it already defaults to "pending").

## Decisions

- **Display string**: Use the lowercase word "pending" for pending status, matching the natural language used by the `--status pending` filter and the `Status` enum value.
- **Single source of truth**: The status string is computed inline in both `handle_list` and `handle_show`. No new helper is introduced because the logic is trivial and adding a helper would be over-engineering for this fix.
- **No migration**: The change only affects output formatting. No data migration is needed.

## Risks / Trade-offs

- **Risk**: Tests that assert the exact output format may fail because the pending status string changes from `" "` to `"pending"`.
  **Mitigation**: Update the relevant tests to expect "pending".
- **Risk**: The `Status` column width in the list table is fixed at `<10`. The word "pending" (8 chars) fits within this width, so no column reformatting is needed.

## Migration Plan

No deployment or data migration is required. The change is purely cosmetic and can be released as a patch.

## Open Questions

None. The change is straightforward and the expected behavior is clear from the issue title and existing specs.
