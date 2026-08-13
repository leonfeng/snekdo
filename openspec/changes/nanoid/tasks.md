## Purpose

Define the implementation tasks for the nanoid ID generation change.

## Implementation Steps

### Step 1: Add nanoid dependency

**File**: `pyproject.toml`

Add `nanoid` to the project dependencies:

```toml
[project]
# ... existing fields ...
dependencies = [
    "nanoid>=3.0",
]
```

Or if using the existing format:

```toml
[project]
# ... existing fields ...
```

Add to dependencies list if it exists, or create the dependencies list.

### Step 2: Update Todo model to use nanoid

**File**: `snekdo/models.py`

Replace the `uuid` import with `nanoid`:

```python
# Remove:
# import uuid

# Add:
from nanoid import nanoid
```

Update the `Todo.__init__` method to use `nanoid()` for default ID generation:

```python
def __init__(
    self,
    id: str = None,
    title: str = "",
    description: str = "",
    due: Optional[str] = None,
    completed: bool = False,
    created_at: Optional[str] = None,
    priority: str = "medium",
) -> None:
    self.id = id or nanoid()
    # ... rest of __init__ ...
```

### Step 3: Update test fixtures

**File**: `tests/test_cli.py`

Replace `str(uuid.uuid4())` with `nanoid()` in the test file:

```python
# Remove:
# import uuid
# ...
# todo = Todo(
#     id=str(uuid.uuid4()),
#     ...
# )

# Add:
from nanoid import nanoid
# ...
todo = Todo(
    id=nanoid(),
    ...
)
```

Update any test fixtures that use UUID-format strings (e.g., `"550e7c9a-6b8a-4d3e-9b5e-8f7d6c5b4a3e"`) to use simpler test IDs (e.g., `"test-id-1"`, `"abc123"`).

### Step 4: Run tests

**Command**:

```bash
pytest
```

Verify all tests pass after the changes.

## Verification

- [x] `nanoid` is listed in `pyproject.tom` dependencies
- [x] `snekdo/models.py` imports `nanoid` instead of `uuid`
- [x] `Todo` objects created without an `id` parameter get a nanoid-format ID
- [x] Tests use nanoid-compatible IDs
- [x] All tests pass with `pytest`
