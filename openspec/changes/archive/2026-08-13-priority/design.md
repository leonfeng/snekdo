## Context

The snekdo application currently supports adding, listing, completing, and deleting todo items. Each todo has an id, title, description, due date, completed status, and created_at timestamp. There is no concept of priority or urgency.

The existing codebase uses Python's standard library, stores data in a local JSON file, and follows a simple CLI pattern with subcommands.

## Goals / Non-Goals

**Goals:**
- Add a `--priority` flag to the `add` command with values: low, medium, high
- Add a `--priority` filter to the `list` command
- Add a `--priority` flag to the `modify` command
- Display priority in list output
- Store priority as a new field on the `Todo` model
- Maintain backward compatibility (default to "medium" for existing todos)

**Non-Goals:**
- Priority-based sorting (e.g., high priority first)
- Priority-based notifications or reminders
- Priority escalation or automation
- Custom priority levels beyond low, medium, high

## Decisions

### Decision: Store priority as a string enum

**Context**: The `Status` enum in `models.py` uses string values for consistency with CLI arguments.

**Decision**: Use a string-based `Priority` enum with values `low`, `medium`, `high`. Store as string in JSON, validate against allowed values.

**Rationale**: Simple, consistent with existing `Status` enum pattern. String values are human-readable in JSON and easy to validate.

**Alternatives considered**:
- Integer priority (0, 1, 2) — less intuitive for users
- Enum class with display names — overkill for three values

### Decision: Default priority is "medium"

**Context**: Existing todos have no priority field.

**Decision**: When creating a new todo without `--priority`, default to "medium". When loading existing todos, treat missing priority as "medium".

**Rationale**: "Medium" is a sensible default that won't surprise users. Existing todos won't be filtered out by default priority filters.

**Alternatives considered**:
- Default to "low" — too passive
- Require priority on create — breaking change, users would need to re-add todos

### Decision: Priority filter is additive with status filter

**Context**: Users may want to filter by both status and priority.

**Decision**: The `list` command supports both `--status` and `--priority` flags. When both are provided, apply both filters (AND logic).

**Rationale**: Users expect filters to compose. A todo can be both "pending" and "high" priority.

**Alternatives considered**:
- Mutually exclusive filters — too restrictive
- OR logic — confusing semantics

### Decision: Priority displayed as short code in list output

**Context**: The list command currently shows ID, Title, Status, Due.

**Decision**: Add a "Priority" column between "Status" and "Due" in the output table.

**Rationale**: Consistent with existing table format. Short codes (L, M, H) save space while being clear.

**Alternatives considerations**:
- Full word "low"/"medium"/"high" — takes too much terminal width
- Color coding — adds complexity, not portable

## Risks / Trade-offs

### Risk: CLI argument parsing complexity
Adding `--priority` to multiple commands increases argument parsing complexity.
→ **Mitigation**: Reuse the same argparse choices validation across commands.

### Risk: Backward compatibility with existing data
Existing todos in JSON have no priority field.
→ **Mitigation**: Use `data.get("priority", "medium")` when deserializing. No data migration needed.

### Risk: User confusion about allowed values
Users may not know the allowed priority values.
→ **Mitigation**: Use argparse `choices` with `metavar` to show help text. Error message will list valid values.

## Open Questions

None.
