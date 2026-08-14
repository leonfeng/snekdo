# list-display Specification

## Purpose

This capability defines the list output display, including the creation date column that shows when each todo was created.

## Requirements

### Requirement: List displays created_at column

The system SHALL display a `Created At` column in the todo list output table showing the creation date/time of each todo.

#### Scenario: Created At column is shown

- **WHEN** user runs `list` command with one or more todos
- **THEN** the output table includes a `Created At` header
- **THEN** each row displays the corresponding todo's `created_at` value

#### Scenario: Created At column is empty for missing dates

- **WHEN** user runs `list` command with a todo that has an empty `created_at`
- **THEN** the `Created At` cell for that todo is empty

#### Scenario: Created At column appears after Due

- **WHEN** user runs `list` command
- **THEN** the `Created At` column appears after the `Due` column

### Requirement: Created At value format

The system SHALL display the `created_at` value in ISO 8601 format as stored.

#### Scenario: ISO 8601 format displayed

- **WHEN** user runs `list` command
- **THEN** the `Created At` column shows the date/time in ISO 8601 format (e.g., `2024-01-01T00:00:00`)

### Requirement: Created At with no todos

The system SHALL display the "No todos found." message when the list is empty, regardless of the created_at display.

#### Scenario: Empty list message

- **WHEN** user runs `list` command with no todos
- **THEN** system displays "No todos found." message
