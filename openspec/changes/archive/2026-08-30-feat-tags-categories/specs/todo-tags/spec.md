## Purpose

Adds free-form `tags` (list of strings) and `category` (single optional string) fields to the Todo model, so users can organize and filter todos beyond priority and due date.

## ADDED Requirements

### Requirement: Todo model stores tags and category

The system SHALL store a `tags` field (list of strings, default empty list) and a `category` field (optional string, default `None`) on each todo.

#### Scenario: New todo defaults

- **WHEN** a todo is created without specifying tags or category
- **THEN** the stored todo has `tags == []` and `category is None`

#### Scenario: New todo with tags and category

- **WHEN** a todo is created with `tags=["work", "urgent"]` and `category="office"`
- **THEN** the stored todo has `tags == ["work", "urgent"]` and `category == "office"`

#### Scenario: Deserializing a stored todo without tags or category

- **WHEN** a JSON todo object without `tags` or `category` keys is loaded
- **THEN** the resulting todo has `tags == []` and `category is None`

#### Scenario: Serialization round-trip preserves tags and category

- **WHEN** a todo with `tags=["a", "b"]` and `category="home"` is serialized via `to_dict()` and deserialized via `from_dict()`
- **THEN** the resulting todo has `tags == ["a", "b"]` and `category == "home"`

### Requirement: CLI add command accepts tags and category

The system SHALL allow users to assign tags and a category when creating a new todo via the `add` command using `--tag` (repeatable) and `--category` flags.

#### Scenario: Add todo with a single tag

- **WHEN** user runs `add` command with `--tag work`
- **THEN** the created todo has `tags == ["work"]`

#### Scenario: Add todo with multiple tags

- **WHEN** user runs `add` command with `--tag work --tag urgent`
- **THEN** the created todo has `tags == ["work", "urgent"]`

#### Scenario: Add todo with category

- **WHEN** user runs `add` command with `--category home`
- **THEN** the created todo has `category == "home"`

#### Scenario: Add todo without tags or category

- **WHEN** user runs `add` command without `--tag` or `--category`
- **THEN** the created todo has `tags == []` and `category is None`

### Requirement: CLI modify command accepts tags and category

The system SHALL allow users to update the tags and category of an existing todo via the `modify` command using `--tag` (repeatable) and `--category` flags.

#### Scenario: Update tags

- **WHEN** user runs `modify` command with `--tag work --tag personal`
- **THEN** the todo's tags are replaced with `["work", "personal"]`

#### Scenario: Update category

- **WHEN** user runs `modify` command with `--category office`
- **THEN** the todo's category is set to `"office"`

#### Scenario: Modify only tags leaves category unchanged

- **WHEN** user runs `modify` command with only `--tag` flags and no `--category`
- **THEN** the todo's category remains unchanged

#### Scenario: Modify only category leaves tags unchanged

- **WHEN** user runs `modify` command with only `--category` and no `--tag` flags
- **THEN** the todo's tags remain unchanged

### Requirement: CLI list command filters by tag and category

The system SHALL allow users to filter the list of todos by tag or category via the `list` command using `--tag` and `--category` flags.

#### Scenario: List todos with a tag

- **WHEN** user runs `list` command with `--tag work`
- **THEN** system displays only todos that contain "work" in their tags

#### Scenario: List todos with a category

- **WHEN** user runs `list` command with `--category home`
- **THEN** system displays only todos whose category is "home"

#### Scenario: List todos with no matching tag

- **WHEN** user runs `list` command with `--tag nonexistent`
- **THEN** system displays "No todos found."

#### Scenario: Tag filter combines with status filter

- **WHEN** user runs `list` command with `--tag work --status pending`
- **THEN** system displays only pending todos that contain "work" in their tags
