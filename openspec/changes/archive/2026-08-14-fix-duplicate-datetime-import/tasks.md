## 1. Fix duplicate datetime import

- [x] 1.1 Remove the redundant `from datetime import datetime` inside `validate_due_date()` in `snekdo/__main__.py` (line 31), keeping the module-level import on line 8.
- [x] 1.2 Verify the file still passes syntax checks and any existing tests.