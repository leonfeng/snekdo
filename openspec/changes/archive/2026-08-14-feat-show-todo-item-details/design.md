## Context

The CLI currently supports `add`, `list`, `complete`, `delete`, and `modify` commands. There is no command to view the full details of a single todo item. The `Todo` model and `TodoStorage` already have all the data needed to display a complete todo record.

## Goals / Non-Goals

**Goals:**
- Add a `show` subcommand that accepts a todo ID and displays all fields
- Reuse the existing `TodoStorage.get()` method to fetch the todo
- Display fields in a labeled format (e.g., "Title: ...")
- Handle the case where the todo is not found

**Non-Goals:**
- No changes to the data model or storage format
- No changes to existing commands
- No batch showing of multiple todos
- No formatting of dates beyond raw ISO 8601 display

## Decisions

### Decision: Use a new `show` subcommand

**Choice**: Add `snekdo show <todo-id>` as a new subcommand.

**Rationale**: 
- Consistent with the existing subcommand pattern (add, list, complete, delete, modify)
- Clear and intuitive for users
- Minimal change to the existing CLI structure

**Alternatives considered**:
- `snekdo detail <todo-id>` - "show" is more standard CLI terminology
- `snekdo list <todo-id>` - would conflict with the existing list command semantics

### Decision: Display format

**Choice**: Use a simple "Label: value" format, one field per line.

**Rationale**: 
- Clear and readable
- Consistent with the project's simple CLI approach
- Easy to test

**Alternatives considered**:
- Table format (used by `list`) - overkill for a single item
- JSON output - not user-friendly for a single item view

### Decision: Error handling

**Choice**: Return exit code 1 and print an error message when the todo is not found.

**Rationale**: 
- Consistent with existing `complete`, `delete`, and `modify` commands
- Allows scripts to detect failures

## Risks / Trade-offs

### Risk: No existing `show` command means users may not discover it

**Impact**: Low - the command is documented in README and `--help`.

**Mitigation**: Document the command in README and help text.

### Risk: Output format may not match user expectations

**Impact**: Low - the format is simple and standard.

**Mitigation**: The format can be adjusted based on user feedback.

## Migration Plan

This is a pure feature addition with no migration required. Existing behavior is preserved.

## Open Questions

None - the implementation approach is clear.
