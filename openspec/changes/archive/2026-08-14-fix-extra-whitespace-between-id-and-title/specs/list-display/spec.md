## ADDED Requirements

### Requirement: ID column width adapts to longest ID

The system SHALL display the ID column wide enough to show the full ID of each todo without truncation, up to a maximum width. When an ID exceeds the maximum column width, the ID SHALL be truncated with an ellipsis (`...`) at the end.

#### Scenario: Short ID is fully visible

- **WHEN** user runs `list` command with a todo whose ID is shorter than the column maximum width
- **THEN** the full ID is displayed in the ID column without truncation

#### Scenario: Long ID is truncated with ellipsis

- **WHEN** user runs `list` command with a todo whose ID exceeds the maximum ID column width
- **THEN** the ID is truncated with an ellipsis (`...`) at the end

#### Scenario: Column width is computed from content

- **WHEN** user runs `list` command with multiple todos of varying ID lengths
- **THEN** the ID column width is wide enough to display the longest non-truncated ID

### Requirement: List output remains aligned after ID width adjustment

The system SHALL keep all columns aligned in the output table after the ID column width is adjusted.

#### Scenario: Table header aligns with data rows

- **WHEN** user runs `list` command
- **THEN** the column headers align with the corresponding data rows
