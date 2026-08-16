## Tasks

- [x] 1.1 Add `playwright` to `pyproject.toml` `[project.optional-dependencies]` → `dev`
- [x] 1.2 Create `tests/e2e/` directory with `__init__.py` and `conftest.py`
- [x] 2.1 `tests/e2e/test_profile.py`: change password (valid + wrong current + short + mismatch)

## Verification

- [x] Run `pytest tests/e2e/test_profile.py -k "test_change_password"` to verify password tests pass