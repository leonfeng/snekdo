## Tasks

- [x] 1.1 Add `playwright` to `pyproject.toml` `[project.optional-dependencies]` → `dev`
- [x] 1.2 Create `tests/e2e/` directory with `__init__.py` and `conftest.py`
- [x] 2.1 `tests/e2e/test_todos.py`: add todo (valid + empty title error)

## Verification

- [x] Run `pytest tests/e2e/test_todos.py -k "test_add_todo"` to verify add todo tests pass