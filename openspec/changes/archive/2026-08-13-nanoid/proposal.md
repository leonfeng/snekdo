## Why

The application currently uses `uuid.uuid4()` for generating unique IDs, which produces long, URL-unsafe UUIDs (e.g., `550e7c9a-6b8a-4d3e-9b5e-8f7d6c5b4a3e`). Replacing this with nanoid generates shorter, URL-friendly IDs (e.g., `abc123XYZ789`) that are more user-friendly for CLI usage and API responses.

## What Changes

- Replace `uuid.uuid4()` with `nanoid` for ID generation in the `Todo` model
- Update the `id` field to use nanoid's default 21-character format
- Update all tests that create `Todo` objects with UUID-format IDs to use nanoid-compatible IDs
- Update `test_cli.py` to use nanoid instead of `uuid.uuid4()`

## Capabilities

### New Capabilities

- `id-generation`: Define the ID generation strategy for todos, specifying that nanoid should be used instead of UUID

### Modified Capabilities

- `todo-modification`: No requirement changes - the modify command behavior remains the same, only the ID format changes internally

## Impact

- **Affected code**: `snekdo/models.py` (id generation), `tests/test_cli.py` (test fixtures using `uuid.uuid4()`)
- **Dependencies**: Add `nanoid` to project dependencies in `pyproject.toml`
- **Backward compatibility**: Existing todos with UUID-format IDs will continue to work; only newly created IDs will use nanoid format
- **Tests**: Update test fixtures that create `Todo` objects with UUID-format strings
