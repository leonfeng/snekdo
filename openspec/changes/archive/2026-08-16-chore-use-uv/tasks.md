## 1. Update pyproject.toml

- [x] 1.1 Remove the `[build-system]` section (setuptools/wheel not needed for uv).
- [x] 1.2 Keep `[project]` metadata, dependencies, and scripts unchanged.
- [x] 1.3 Keep `[project.optional-dependencies]` (api, test, dev) unchanged.
- [x] 1.4 Keep `[tool.setuptools.packages.find]` removed or replace with uv-compatible package discovery.

## 2. Update Makefile

- [x] 2.1 Replace `ruff check .` with `uv run ruff check .`.
- [x] 2.2 Replace `ruff format .` with `uv run ruff format .`.
- [x] 2.3 Replace `pytest` with `uv run pytest`.

## 3. Update AGENTS.md

- [x] 3.1 Update "Running" section to use `uv pip install` instead of `pip install`.
- [x] 3.2 Document `uv run pytest` for tests.
- [x] 3.3 Document `uv run snekdo` for CLI usage.

## 4. Recreate virtual environment

- [x] 4.1 Remove `.venv` and recreate with `uv venv`.
- [x] 4.2 Install package editable with `uv pip install -e .`.

## 5. Verify

- [x] 5.1 Run `uv run pytest` to confirm tests pass.
- [x] 5.2 Run `snekdo --help` to confirm CLI works.
- [x] 5.3 Run `uv build` to confirm package builds.

## Notes

- **Dependency fix**: `nanoid>=3.0` was changed to `nanoid>=2.0` because `nanoid>=3.0` does not exist on PyPI (only up to 2.0.0 is available). Without this fix, `uv pip install -e .` fails dependency resolution.
- **Missing dependency**: `python-multipart>=0.0.7` was added to `dependencies` because FastAPI form data handling (used by web routes) requires it. This was a pre-existing gap that caused 18 web tests to fail at collection time.
- **Virtual environment**: `.venv` was recreated with `uv venv` (Python 3.13.13) and package installed with `uv pip install -e .`.
- **Verification**: All 188 tests pass with `uv run pytest`; CLI works with `uv run snekdo`; package builds with `uv build`.