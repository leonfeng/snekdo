## Purpose

This capability defines the default filtering behavior of the list command, including hiding completed todo items by default while still allowing users to view them explicitly.

## ADDED Requirements

### Requirement: Hide completed items by default

The system SHALL hide completed todo items from the list output by default when the user runs the `list` command without a status flag.

#### Scenario: Completed items hidden by default

- **WHEN** user runs `list` command without `--status` flag
- **THEN** system displays only pending (non-completed) todos
- **THEN** completed todos are not shown in the output

#### Scenario: All items shown with --status all

- **WHEN** user runs `list --status all`
- **THEN** system displays all todos, including completed ones

#### Scenario: Completed items shown with --status completed

- **WHEN** user runs `list --status completed`
- **THEN** system displays only completed todos

### Requirement: Pending items shown by default

The system SHALL display pending (non-completed) todo items when the user runs the `list` command without a status flag.

#### Scenario: Pending items displayed

- **WHEN** user runs `list` command without `--status` flag
- **THEN** system displays all pending todos

#### Scenario: Empty list when no pending items

- **WHEN** user runs `list` command with no pending todos
- **THEN** system displays "No todos found." message

### Requirement: Default filter applies with sorting and limiting

The system SHALL apply the default completed-item filter before sorting and limiting results.

#### Scenario: Default filter with sort

- **WHEN** user runs `list --sort title` without `--status` flag
- **THEN** system displays only pending todos sorted by title

#### Scenario: Default filter with limit

- **WHEN** user runs `list --limit 5` without `--status` flag
- **THEN** system displays only the top 5 pending todos
