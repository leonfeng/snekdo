## Tasks

- [x] 1.1 Add `playwright` to `pyproject.toml` `[project.optional-dependencies]` → `dev`
- [x] 1.2 Create `tests/e2e/` directory with `__init__.py` and `conftest.py`
- [x] 2.1 `tests/e2e/test_profile.py`: update display name
- [x] 2.2 `tests/e2e/test_profile.py`: update email (valid + invalid format)

## Verification

- [x] Run `pytest tests/e2e/test_profile.py -k "test_update_profile or test_update_email"` to verify update tests pass