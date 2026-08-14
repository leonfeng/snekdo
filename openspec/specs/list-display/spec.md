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

### Requirement: List displays status column

The system SHALL display a `Status` column in the todo list output table showing the completion status of each todo.

#### Scenario: Status column is shown

- **WHEN** user runs `list` command with one or more todos
- **THEN** the output table includes a `Status` header
- **THEN** each row displays the corresponding todo's status

#### Scenario: Pending status is displayed as text

- **WHEN** user runs `list` command with a pending todo
- **THEN** the `Status` cell for that todo displays "pending"

#### Scenario: Completed status is displayed as checkmark

- **WHEN** user runs `list` command with a completed todo
- **THEN** the `Status` cell for that todo displays "✓"

#### Scenario: Status column appears before Priority

- **WHEN** user runs `list` command
- **THEN** the `Status` column appears before the `Priority` column

### Requirement: Title column adapts to long titles

The system SHALL display the Title column wide enough to show the full title of each todo without truncation, up to a maximum width. When a title exceeds the maximum column width, the title SHALL be truncated with an ellipsis (`...`) at the end.

#### Scenario: Short title is fully visible

- **WHEN** user runs `list` command with a todo whose title is shorter than the column maximum width
- **THEN** the full title is displayed in the Title column without truncation

#### Scenario: Long title is truncated with ellipsis

- **WHEN** user runs `list` command with a todo whose title exceeds the maximum Title column width
- **THEN** the title is truncated with an ellipsis (`...`) at the end

#### Scenario: Column width is computed from content

- **WHEN** user runs `list` command with multiple todos of varying title lengths
- **THEN** the Title column width is wide enough to display the longest non-truncated title

### Requirement: List output remains aligned

The system SHALL keep all columns aligned in the output table after the Title column width is adjusted.

#### Scenario: Table header aligns with data rows

- **WHEN** user runs `list` command
- **THEN** the column headers align with the corresponding data rows
