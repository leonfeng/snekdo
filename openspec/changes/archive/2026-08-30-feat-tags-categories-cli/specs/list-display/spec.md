## ADDED Requirements

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
