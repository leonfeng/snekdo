## Approach

This change removes unused imports from all Python files in the project. The approach is mechanical and low-risk:

1. **Identify unused imports**: Use Python's `ast` module to parse each `.py` file, collect all imported names, and determine which are never referenced in the AST (excluding `from __future__ import annotations` which is a special directive).
2. **Remove unused imports**: Edit each file to remove the unused import lines, preserving the import style (grouping, ordering).
3. **Verify**: Run the existing test suite to confirm no behavior changes.

## Files and Unused Imports

| File | Unused Imports |
|------|---------------|
| `snekdo/__main__.py` | `import json`, `from typing import Optional` |
| `snekdo/models.py` | `from dataclasses import field`, `from datetime import datetime` |
| `tests/test_cli.py` | `from pathlib import Path`, `import sys`, `from io import StringIO`, `from contextlib import contextmanager`, `import pytest`, `from snekdo.storage import TodoStorage` |
| `tests/test_storage.py` | `import json` |

Note: `from __future__ import annotations` is a special future-import directive and is intentionally preserved.

## Risk Assessment

- **Low risk**: Removing unused imports does not change runtime behavior.
- All type hints, function signatures, and imports that are actually used are preserved.
- The test suite should pass without modification.
