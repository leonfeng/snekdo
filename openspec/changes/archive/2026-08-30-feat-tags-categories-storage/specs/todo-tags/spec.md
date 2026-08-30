## Purpose

Defines how `tags` and `category` are persisted across both storage backends and carried through recurrence.

## ADDED Requirements

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
