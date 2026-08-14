## Why

The application currently uses `uuid.uuid4()` for generating unique IDs, producing 36-character strings like `550e7c9a-6b8a-4d3e-9b5e-8f7d6c5b4a3e`. These are:
- Too long for comfortable display in CLI output
- URL-unfriendly due to hyphens
- Not human-readable or memorable

nanoid produces 21-character URL-safe strings (e.g., `NktU7i6RVn7wDZe`) that are:
- Shorter and more compact
- URL-safe (no special characters)
- Still cryptographically secure and unique

## What Changes

- Replace `uuid` import with `nanoid` import in `snekdo/models.py`
- Update `Todo` class to use `nanoid()` for ID generation
- Update test fixtures in `tests/test_cli.py` to use nanoid-compatible IDs
- Add `nanoid` dependency to `pyproject.toml`

## How

### ID Generation Strategy

Use nanoid's default configuration (21 characters, URL-safe alphabet) for generating unique IDs:

```python
from nanoid import nanoid

class Todo:
    def __init__(self, id: str = None, ...):
        self.id = id or nanoid()
```

### Files to Modify

1. **snekdo/models.py** - Replace `uuid` import with `nanoid`, update `Todo.__init__` to use `nanoid()` for default ID generation
2. **pyproject.toml** - Add `nanoid` to project dependencies
3. **tests/test_cli.py** - Update test fixtures that create `Todo` objects with UUID-format strings

### Test Updates

- `test_cli.py` line 47: Replace `str(uuid.uuid4())` with `nanoid()`
- All test fixtures using UUID-format IDs (e.g., `"550e7c9a-6b8a-4d3e-9b5e-8f7d6c5b4a3e"`) should be updated to use nanoid-format IDs (e.g., `"test-id-1"`, `"abc123"`)

## Design Decisions

### Why nanoid over UUID?

1. **Readability**: 21 characters vs 36 characters for UUID
2. **URL-safe**: No hyphens, just alphanumeric
3. **Standard in Python ecosystem**: Well-maintained package
4. **Backward compatible**: Existing UUID-format IDs in storage continue to work

### Why not modify existing IDs?

Changing existing IDs would break references and require data migration. The safer approach is:
- Keep existing UUID-format IDs as-is
- Generate new IDs using nanoid
- This is a common pattern for ID format changes

### Implementation Approach

1. Add `nanoid` dependency
2. Update `Todo` model to use `nanoid()` for default ID generation
3. Update tests to use nanoid-compatible IDs
4. No changes needed to storage layer (it just stores whatever ID is provided)

## Constraints

- Must maintain backward compatibility with existing UUID-format IDs
- Must not change the `Todo` class interface (still accepts `id` parameter)
- Must not change storage format or behavior
- Must not change CLI commands or their behavior
