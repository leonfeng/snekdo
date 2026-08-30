## MODIFIED Requirements

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

## ADDED Requirements

### Requirement: List displays Tags column

The system SHALL display a `Tags` column in the todo list output table. The value SHALL be the todo's tags joined by `", "` (comma-space). When a todo has no tags, the cell SHALL be empty. The column SHALL be truncated with `...` if it exceeds 30 characters.

#### Scenario: Tags column shows comma-separated tags

- **WHEN** user runs `list` command with a todo that has `tags=["work", "urgent"]`
- **THEN** the `Tags` cell displays `work, urgent`

#### Scenario: Tags column is empty when no tags

- **WHEN** user runs `list` command with a todo that has `tags=[]`
- **THEN** the `Tags` cell is empty

#### Scenario: Tags column is truncated when long

- **WHEN** user runs `list` command with a todo whose joined tags exceed 30 characters
- **THEN** the `Tags` cell is truncated with `...` at the end

#### Scenario: Tags column appears after Created At

- **WHEN** user runs `list` command
- **THEN** the `Tags` column appears after the `Created At` column

### Requirement: List displays Category column

The system SHALL display a `Category` column in the todo list output table. The value SHALL be the todo's category string. When a todo has no category (`None`), the cell SHALL be empty.

#### Scenario: Category column shows the category

- **WHEN** user runs `list` command with a todo that has `category="work"`
- **THEN** the `Category` cell displays `work`

#### Scenario: Category column is empty when no category

- **WHEN** user runs `list` command with a todo that has `category=None`
- **THEN** the `Category` cell is empty

#### Scenario: Category column appears after Tags

- **WHEN** user runs `list` command
- **THEN** the `Category` column appears after the `Tags` column

### Requirement: List filters by tag

The system SHALL allow filtering the list output by a single tag using the `--tag` flag. A todo matches if the given tag is present in its `tags` list.

#### Scenario: Filter by an existing tag

- **WHEN** user runs `list --tag work` and there exist todos with "work" in their tags
- **THEN** only those todos are displayed

#### Scenario: Filter by a tag that matches no todo

- **WHEN** user runs `list --tag nonexistent`
- **THEN** the output shows "No todos found."

#### Scenario: Tag filter combines with status filter

- **WHEN** user runs `list --tag work --status pending`
- **THEN** only pending todos whose tags include "work" are displayed

### Requirement: List filters by category

The system SHALL allow filtering the list output by an exact category using the `--category` flag.

#### Scenario: Filter by an existing category

- **WHEN** user runs `list --category work` and there exist todos with `category="work"`
- **THEN** only those todos are displayed

#### Scenario: Filter by a category that matches no todo

- **WHEN** user runs `list --category nonexistent`
- **THEN** the output shows "No todos found."

#### Scenario: Category filter combines with status filter

- **WHEN** user runs `list --category home --status completed`
- **THEN** only completed todos whose category is "home" are displayed
