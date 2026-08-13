# Design: Todo Modification Feature

## Context

The snekdo application currently supports basic CRUD operations (Create, Read, Delete) with a special case for completing todos. There is no update capability for modifying existing todo attributes. This design addresses that gap by adding a `modify` command that allows users to update todo items.

## Goals / Non-Goals

**Goals:**
- Add a `modify` command to update existing todo items
- Support updating title, description, due date, and other attributes
- Maintain consistency with existing CLI patterns
- Provide clear error messages for invalid operations
- Ensure data integrity during updates

**Non-Goals:**
- Adding complex validation rules beyond required fields
- Supporting batch updates of multiple todos
- Adding undo/rollback functionality
- Changing existing command behavior

## Decisions

### Decision 1: Use Optional Arguments for Selective Updates
**Choice**: Use optional arguments for the modify command, allowing users to update only the fields they want to change.

**Rationale**: This provides flexibility and matches common CLI patterns (e.g., `git commit --message`). Users can update just the title, or just the due date, or all fields in one command.

**Alternatives considered**:
- Required arguments: Would force users to provide all fields even when only updating one
- Full object replacement: Would require providing all fields even when updating one

### Decision 2: Store and Update Pattern
**Choice**: Implement a `modify()` method in `TodoStorage` that loads all todos, finds the target by ID, updates the in-memory object, and saves all todos back.

**Rationale**: This approach is consistent with existing methods like `complete()` and `delete()`. It's simple and maintains the existing architecture.

**Alternatives considered**:
- Direct database update: Would require SQL or more complex storage layer
- In-place file editing: More complex and error-prone

### Decision 3: CLI Argument Structure
**Choice**: Use `snekdo modify <todo-id> [--title "New Title"] [--description "New Description"] [--due "2024-12-31"]`

**Rationale**: This structure is intuitive and follows the pattern of other commands. The ID is required, while update fields are optional.

**Alternatives considered**:
- Positional arguments for all fields: Less flexible
- Subcommand per field: Overly complex

## Risks / Trade-offs

- **Risk**: Users might accidentally overwrite data
  - **Mitigation**: Clear error messages and help text. No undo, but that's consistent with existing commands.

- **Risk**: Concurrent modification could cause data loss
  - **Mitigation**: Existing file locking mechanism should handle this, but worth monitoring.

- **Risk**: Invalid date format could break existing functionality
  - **Mitigation**: Basic validation in the CLI layer before calling storage.

## Migration Plan

This is a backward-compatible addition. No migration needed for existing data.

**Deployment steps**:
1. Add `modify` command to CLI
2. Add `modify()` method to storage
3. Add tests
4. Update documentation

**Rollback strategy**: Since this adds new functionality without modifying existing behavior, rollback is as simple as not using the new command.

## Open Questions

None - all requirements are clear from the user story.
