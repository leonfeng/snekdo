## ADDED Requirements

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

## REMOVED Requirements

### Requirement: Fixed title width

**Reason**: Replaced by adaptive title column width to support long titles.
**Migration**: No migration needed; the list command continues to display titles, now without silent truncation.
