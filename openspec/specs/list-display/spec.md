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

### Requirement: List output remains aligned

The system SHALL keep all columns aligned in the output table after the Title column width is adjusted.

#### Scenario: Table header aligns with data rows

- **WHEN** user runs `list` command
- **THEN** the column headers align with the corresponding data rows

### Requirement: List output remains aligned after ID width adjustment

The system SHALL keep all columns aligned in the output table after the ID column width is adjusted.

#### Scenario: Table header aligns with data rows

- **WHEN** user runs `list` command
- **THEN** the column headers align with the corresponding data rows

### Requirement: List displays Tags column

The system SHALL display a `Tags` column in the todo list output after `Created At`. Tags are joined with `", "` and truncated with `...` when exceeding 30 characters.

#### Scenario: Tags column shows comma-separated tags

- **WHEN** user runs `list` command with a todo that has `tags=["work", "urgent"]`
- **THEN** the `Tags` cell displays `work, urgent`

#### Scenario: Tags column empty for no tags

- **WHEN** user runs `list` command with a todo that has no tags
- **THEN** the `Tags` cell is empty

#### Scenario: Tags column truncated when long

- **WHEN** user runs `list` command with a todo whose joined tags exceed 30 characters
- **THEN** the `Tags` cell is truncated with `...` at the end

### Requirement: List displays Category column

The system SHALL display a `Category` column in the todo list output after `Tags`. Empty when category is not set.

#### Scenario: Category column shows the category

- **WHEN** user runs `list` command with a todo that has `category="work"`
- **THEN** the `Category` cell displays `work`

#### Scenario: Category column empty when no category

- **WHEN** user runs `list` command with a todo that has no category
- **THEN** the `Category` cell is empty

### Requirement: List filters by tag

The system SHALL allow filtering list output by a single tag using the `--tag` flag. A todo matches if the given tag is present in its tags list.

#### Scenario: Filter by an existing tag

- **WHEN** user runs `list --tag work` and todos with "work" in their tags exist
- **THEN** only todos containing "work" in their tags are displayed

#### Scenario: Filter by a tag matching no todos

- **WHEN** user runs `list --tag nonexistent`
- **THEN** system displays "No todos found."

#### Scenario: Tag filter combines with status filter

- **WHEN** user runs `list --tag work --status pending`
- **THEN** only pending todos that contain "work" in their tags are displayed

### Requirement: List filters by category

The system SHALL allow filtering list output by an exact category using the `--category` flag.

#### Scenario: Filter by an existing category

- **WHEN** user runs `list --category home` and todos with `category="home"` exist
- **THEN** only those todos are displayed

#### Scenario: Filter by a non-existent category

- **WHEN** user runs `list --category nonexistent`
- **THEN** system displays "No todos found."

#### Scenario: Category filter combines with status filter

- **WHEN** user runs `list --category home --status completed`
- **THEN** only completed todos whose category is "home" are displayed
