## Tasks

- [x] 1.1 Add `playwright` to `pyproject.toml` `[project.optional-dependencies]` → `dev`
- [x] 1.2 Create `tests/e2e/` directory with `__init__.py` and `conftest.py`
- [x] 2.1 `tests/e2e/test_todos.py`: empty list placeholder
- [x] 2.2 `tests/e2e/test_todos.py`: list page shows todo rows

## Verification

- [x] Run `pytest tests/e2e/test_todos.py -k "empty_list or test_list_shows_todo_rows"` to verify list tests pass