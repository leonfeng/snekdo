## MODIFIED Requirements

### Requirement: Add todo form includes all optional fields

The add form SHALL present input fields for title (required), description, due date, priority, repeat, tags (comma-separated), and category.

#### Scenario: Add form renders new inputs

- **WHEN** a user visits the add page
- **THEN** the form includes a text input for `tags` (placeholder "work, personal") and a text input for `category` (placeholder "e.g., office")

#### Scenario: Add with tags and category

- **WHEN** a user submits the add form with tags "work, urgent" and category "office"
- **THEN** the created todo has `tags == ["work", "urgent"]` and `category == "office"`

#### Scenario: Add with empty tags and category

- **WHEN** a user submits the add form with empty tags and category fields
- **THEN** the created todo has `tags == []` and `category is None`

#### Scenario: Add trims whitespace in tags

- **WHEN** a user submits the add form with tags " work ,  urgent "
- **THEN** the created todo has `tags == ["work", "urgent"]`

### Requirement: Edit form includes tags and category inputs

The edit form SHALL include a `tags` input pre-filled with the comma-separated existing tags and a `category` input pre-filled with the existing category (empty when None).

#### Scenario: Edit form pre-fills tags and category

- **WHEN** a user opens the edit page for a todo with `tags=["work","home"]` and `category="office"`
- **THEN** the tags input contains "work, home" and the category input contains "office"

#### Scenario: Edit updates tags and category

- **WHEN** a user submits the edit form with new tags "urgent" and category "home"
- **THEN** the todo is updated to `tags == ["urgent"]` and `category == "home"`

### Requirement: List view displays tags and category columns

The list view SHALL display a `Tags` column and a `Category` column after `Created At`, with empty cells when a todo has no tags or category.

#### Scenario: List shows tags and category

- **WHEN** a user views the list page with a todo having tags and a category
- **THEN** the row displays the comma-joined tags in the Tags column and the category in the Category column

#### Scenario: List shows empty cells for missing tags/category

- **WHEN** a user views the list page with a todo that has no tags and no category
- **THEN** the Tags and Category cells are empty
