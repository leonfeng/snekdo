## Purpose

This capability adds priority levels (low, medium, high) to todo items, allowing users to set, filter, and display the priority of their todos.

## Requirements

### Requirement: Add priority when creating a todo

The system SHALL allow users to specify a priority level when creating a new todo item via the `--priority` flag.

#### Scenario: Create todo with high priority

- **WHEN** user runs `add` command with `--priority high`
- **THEN** system creates the todo with priority set to "high"

#### Scenario: Create todo with default priority

- **WHEN** user runs `add` command without specifying `--priority`
- **THEN** system creates the todo with priority set to "medium"

#### Scenario: Create todo with low priority

- **WHEN** user runs `add` command with `--priority low`
- **THEN** system creates the todo with priority set to "low"

### Requirement: Filter todos by priority

The system SHALL allow users to filter the list of todos by priority level.

#### Scenario: List todos with high priority

- **WHEN** user runs `list` command with `--priority high`
- **THEN** system displays only todos with priority "high"

#### Scenario: List todos with medium priority

- **WHEN** user runs `list` command with `--priority medium`
- **THEN** system displays only todos with priority "medium"

#### Scenario: List todos with low priority

- **WHEN** user runs `list` command with `--priority low`
- **THEN** system displays only todos with priority "low"

#### Scenario: List todos with invalid priority

- **WHEN** user runs `list` command with an invalid `--priority` value
- **THEN** system displays an error message and returns non-zero exit code

### Requirement: Display priority in list output

The system SHALL display the priority level of each todo item in the list output.

#### Scenario: Display priority column

- **WHEN** user runs `list` command
- **THEN** system displays a priority column showing the priority level of each todo

#### Scenario: Display priority for todos with different priorities

- **WHEN** user runs `list` command with todos of varying priorities
- **THEN** system displays the correct priority level for each todo

### Requirement: Modify priority of existing todo

The system SHALL allow users to update the priority of an existing todo via the `modify` command.

#### Scenario: Update priority to high

- **WHEN** user runs `modify` command with `--priority high`
- **THEN** system updates the todo's priority to "high"

#### Scenario: Update priority to low

- **WHEN** user runs `modify` command with `--priority low`
- **THEN** system updates the todo's priority to "low"

#### Scenario: Update priority to medium

- **WHEN** user runs `modify` command with `--priority medium`
- **THEN** system updates the todo's priority to "medium"

#### Scenario: Modify non-existent todo priority

- **WHEN** user runs `modify` command with `--priority` for a todo that does not exist
- **THEN** system displays an error message and returns non-zero exit code

### Requirement: Validate priority values

The system SHALL validate that priority values are one of: low, medium, high.

#### Scenario: Invalid priority value

- **WHEN** user provides an invalid priority value (e.g., "urgent", "critical")
- **THEN** system displays an error message and returns non-zero exit code

#### Scenario: Empty priority value

- **WHEN** user provides an empty `--priority` value
- **THEN** system displays an error message and returns non-zero exit code
