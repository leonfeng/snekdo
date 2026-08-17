## Purpose

Defines the serialization and deserialization contract for the `Todo` model, ensuring that nullable fields are normalized consistently when loading from and saving to JSON storage.

## Requirements

### Requirement: from_dict normalizes empty strings to None for nullable fields

The system SHALL convert empty-string values to `None` (Python `None`) for nullable `Todo` fields (`due` and `user_id`) when deserializing from a dict loaded from JSON.

#### Scenario: Empty string due becomes None

- **WHEN** `Todo.from_dict()` is called with `{"due": ""}`
- **THEN** the resulting `Todo` has `due is None`

#### Scenario: Empty string user_id becomes None

- **WHEN** `Todo.from_dict()` is called with `{"user_id": ""}`
- **THEN** the resulting `Todo` has `user_id is None`

#### Scenario: Missing fields use defaults

- **WHEN** `Todo.from_dict()` is called with a dict missing `due` and `user_id`
- **THEN** `due` is `None` and `user_id` is `None`

#### Scenario: Valid values are preserved

- **WHEN** `Todo.from_dict()` is called with `{"due": "2024-12-31", "user_id": "user123"}`
- **THEN** `due == "2024-12-31"` and `user_id == "user123"`

#### Scenario: Null values are preserved

- **WHEN** `Todo.from_dict()` is called with `{"due": None, "user_id": None}`
- **THEN** `due is None` and `user_id is None`
