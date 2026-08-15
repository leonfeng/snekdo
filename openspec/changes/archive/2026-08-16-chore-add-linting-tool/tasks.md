## 1. Add ruff dependency and configuration

- [x] 1.1 Add `ruff` to `[project.optional-dependencies]` as `dev` in `pyproject.toml`
- [x] 1.2 Add `[tool.ruff]` configuration section to `pyproject.toml` with PEP 8 and common rules
- [x] 1.3 Add a `lint` target to `Makefile` or a shell script for running `ruff check`

## 2. Run lint and fix violations

- [x] 2.1 Run `ruff check .` to identify all violations in the codebase
- [x] 2.2 Fix any import ordering issues (use `ruff check --fix` if safe)
- [x] 2.3 Fix any style violations that cannot be auto-fixed
- [x] 2.4 Run `ruff check .` again to verify all violations are resolved

## 3. Finalize

- [x] 3.1 Run `pytest` to ensure no tests are broken by the linting changes
- [x] 3.2 Update `pytest.ini` if needed (no changes needed if ruff is only a dev dep)
- [x] 3.3 Commit the changes
