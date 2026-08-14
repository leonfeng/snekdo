## Context

The `list` command in `snekdo/__main__.py` currently defaults to showing all todos (`--status all` behavior). The filtering logic already supports `pending`, `completed`, and `all` statuses via the `--status` flag. The default value of the `--status` argument is currently `"all"`.

## Goals / Non-Goals

**Goals:**
- Change the default value of `--status` from `"all"` to `"pending"`
- Ensure the existing `--status all` and `--status completed` flags still work as expected
- Update tests and documentation to reflect the new default

**Non-Goals:**
- No changes to the filtering logic itself (it already supports pending/completed/all)
- No changes to sorting, limiting, or other list features
- No new CLI flags

## Decisions

### Decision: Change default status value

**Choice**: Change the `default="all"` to `default="pending"` on the `--status` argument in the `list` subparser.

**Rationale**: 
- Minimal code change - the filtering logic already handles "pending" correctly
- The existing `--status` argument already has choices=["all", "pending", "completed"]
- This is the simplest and most intuitive change

**Alternatives considered**:
- Add a new `--hide-completed` flag - more complex, less intuitive
- Change the default in `handle_list` instead of the parser - less explicit

### Decision: No change to filtering logic

**Choice**: The existing filter logic in `handle_list` already correctly filters by status. No changes needed.

**Rationale**: The existing code already filters by status correctly; only the default needs to change.

## Risks / Trade-offs

### Risk: Backward compatibility

**Impact**: Medium - users who rely on `list` showing all todos by default will see a change in behavior.

**Mitigation**: The change is documented in README and help text. Users can still use `--status all` to see all todos.

### Risk: Existing tests may fail

**Impact**: Medium - tests that expect all todos to be shown by default will need updating.

**Mitigation**: Update existing tests to use `--status all` where appropriate.

## Migration Plan

This is a behavior change with no data migration required.

## Open Questions

None - the implementation approach is clear.
