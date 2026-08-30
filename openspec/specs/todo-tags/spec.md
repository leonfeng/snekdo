# Spec: todo-tags

## Purpose

Adds `tags` (list of strings) and `category` (optional string) to the Todo model for organizing and filtering todos.

## Requirements

### Requirement: Todo stores tags and category

The `Todo` model SHALL include a `tags` field (list of strings, default empty list) and a `category` field (string or None, default None).

#### Scenario: New todo defaults

- **WHEN** a Todo is instantiated without tags or category
- **THEN** `tags` equals `[]` and `category` is `None`

#### Scenario: Todo with tags and category

- **WHEN** a Todo is instantiated with `tags=["work","urgent"]` and `category="office"`
- **THEN** the stored todo has those exact values

### Requirement: Serialization includes tags and category

`to_dict()` SHALL serialize `tags` and `category`. `from_dict()` SHALL restore them, defaulting to `[]` and `None` when keys are absent.

#### Scenario: Round-trip preserves values

- **WHEN** a todo with `tags=["a","b"]` and `category="home"` is serialized and deserialized
- **THEN** the resulting todo has `tags == ["a","b"]` and `category == "home"`

#### Scenario: Old-format JSON loads without error

- **WHEN** a JSON todo object without `tags` or `category` keys is deserialized
- **THEN** the resulting todo has `tags == []` and `category is None`

### Requirement: Tags and category persist in JSON storage

The system SHALL persist `tags` and `category` in the JSON storage file so they survive load/save cycles.

#### Scenario: Round-trip through JSON

- **WHEN** a todo with `tags=["a","b"]` and `category="home"` is saved and reloaded
- **THEN** both fields are preserved exactly

#### Scenario: Old JSON file without keys loads correctly

- **WHEN** a storage file is loaded that was written before this feature (no `tags` or `category` keys)
- **THEN** todos load with `tags == []` and `category is None`

### Requirement: Tags and category persist in SQLite storage

The system SHALL store `tags` (JSON-encoded list in a TEXT column) and `category` (TEXT) in the SQLite backend.

#### Scenario: Round-trip through SQLite

- **WHEN** a todo with tags and category is added via the SQLite backend and retrieved
- **THEN** both fields are preserved

### Requirement: Existing SQLite databases migrate in place

The system SHALL add the `tags` and `category` columns to a pre-existing SQLite database without data loss.

#### Scenario: Migration on existing DB

- **WHEN** the app initializes against a SQLite DB created before this feature
- **THEN** the `tags` column defaults to `[]` and `category` column to `NULL` for existing rows, and all existing todos remain queryable

### Requirement: Modify updates tags and category

The storage layer `modify` operation SHALL support updating `tags` (replacing the full list) and `category`.

#### Scenario: Replace tags via modify

- **WHEN** a modify operation passes `tags=["x","y"]`
- **THEN** the todo's tag list becomes `["x","y"]`, replacing any previous tags

#### Scenario: Clear category via modify

- **WHEN** a modify operation passes `category=None`
- **THEN** the todo's category is cleared

### Requirement: Recurrence copies tags and category

When a recurring todo is completed and the next occurrence is created, the new occurrence SHALL copy `tags` and `category` from the source.

#### Scenario: Next occurrence inherits tags and category

- **WHEN** a recurring todo with `tags=["work"]` and `category="office"` is completed
- **THEN** the newly created pending occurrence has `tags=["work"]` and `category="office"`
