## Implementation Tasks

- [x] Remove unused imports from `snekdo/__main__.py`:
  - Remove `import json`
  - Remove `from typing import Optional`

- [x] Remove unused imports from `snekdo/models.py`:
  - Change `from dataclasses import dataclass, field` to `from dataclasses import dataclass`
  - Remove `from datetime import datetime`

- [x] Remove unused imports from `tests/test_cli.py`:
  - Remove `from pathlib import Path`
  - Remove `import sys`
  - Remove `from io import StringIO`
  - Remove `from contextlib import contextmanager`
  - Remove `import pytest`
  - Remove `from snekdo.storage import TodoStorage`

- [x] Remove unused imports from `tests/test_storage.py`:
  - Remove `import json`

- [x] Verify the test suite passes:
  - Run `pytest` and confirm all tests pass.

- [x] Run a final lint check (if available) to confirm no unused imports remain.
