## Why

`Todo.from_dict()` deserializes stored JSON into `Todo` objects, but it does not normalize empty-string values to `None` for nullable fields. The `due` field is already normalized (`data.get("due") or None`), but `user_id` is not (`data.get("user_id")`), so a stored `user_id: ""` produces a `Todo` with `user_id == ""` instead of `None`. This inconsistency breaks the web UI's user-filtering logic and creates mixed `null`/`""` values in storage.

## What Changes

- Update `Todo.from_dict()` in `snekdo/models.py` to convert empty strings to `None` for nullable fields (`due` and `user_id`).
- Add a new spec capability `todo-model` describing the normalization requirement.
- Add/update tests to verify empty-string normalization for both `due` and `user_id`.

## Capabilities

### New Capabilities

- `todo-model`: Defines the serialization/deserialization contract for the `Todo` model, including normalization of empty strings to `None` for nullable fields.

### Modified Capabilities

- `api-due-date-completed`: Add a requirement that `Todo.from_dict()` normalizes empty strings to `None` (extends the existing due-date normalization requirement).

## Impact

- `snekdo/models.py`: `Todo.from_dict()` normalization logic.
- `snekdo/storage.py`: `Todo.from_dict()` is used when loading todos from JSON.
- `snekdo/__main__.py`: `Todo.from_dict()` is used during sync.
- `tests/test_models.py`: New/updated tests for empty-string normalization.
- Web UI filtering by `user_id` becomes reliable since `None` and `""` are treated consistently.
