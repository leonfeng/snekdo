## Purpose

Adds `tags` (list of strings) and `category` (optional string) to the Todo model for organizing and filtering todos.

## ADDED Requirements

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
