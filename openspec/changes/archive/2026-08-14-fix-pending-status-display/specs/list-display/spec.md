## MODIFIED Requirements

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
