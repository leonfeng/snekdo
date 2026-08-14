## ADDED Requirements

### Requirement: Column whitespace is uniform

The system SHALL display uniform whitespace between all columns in the todo list output table. Each column cell SHALL be padded to its computed or fixed width with a single space separator between columns.

#### Scenario: Uniform spacing between columns

- **WHEN** user runs `list` command with multiple todos
- **THEN** the whitespace between every column in the header and data rows is consistent

#### Scenario: Fixed-width columns use consistent padding

- **WHEN** user runs `list` command
- **THEN** columns with fixed widths (Status, Priority, Due, Created At) are padded to their fixed width with a single space separator

#### Scenario: Dynamic-width columns use consistent padding

- **WHEN** user runs `list` command with todos of varying title lengths
- **THEN** the ID and Title columns are padded to their computed width with a single space separator

### Requirement: Table header aligns with data rows

The system SHALL keep all columns aligned in the output table.

#### Scenario: Header aligns with data rows

- **WHEN** user runs `list` command
- **THEN** the column headers align with the corresponding data rows

## REMOVED Requirements

### Requirement: Fixed title width

**Reason**: Replaced by adaptive title column width to support long titles.
**Migration**: No migration needed; the list command continues to display titles, now without silent truncation.
