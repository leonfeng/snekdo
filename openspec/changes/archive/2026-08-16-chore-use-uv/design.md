## Context

The project uses `setuptools` as its build backend in `pyproject.toml`. The goal is to migrate to `uv` as the build/packaging tool while preserving all existing functionality and dependencies.

## Goals / Non-Goals

**Goals:**
- Replace `setuptools` build system with `uv`-compatible configuration.
- Update documentation (`Makefile`, `AGENTS.md`) to use `uv` commands.
- Ensure the project still installs and runs correctly with `uv`.

**Non-Goals:**
- No changes to application logic, CLI behavior, API, or data models.
- No new features or refactoring of existing code.

## Decisions

- Use `uv`'s native `pyproject.toml` support (no `build-backend` needed; `uv` can build directly from `pyproject.toml`).
- Keep the same dependency versions and extras (`api`, `test`, `dev`).
- Use `uv pip install -e .` for editable installs and `uv run pytest` for running tests.
- Remove `setuptools` and `wheel` from build-system requirements since `uv` doesn't need them.

## Risks / Trade-offs

- [Risk] `uv` may handle editable installs slightly differently than `pip install -e`. → Mitigation: test `uv pip install -e .` and verify `snekdo` CLI is available.
- [Risk] Some tooling in the ecosystem may still expect setuptools. → Mitigation: this project only needs to build/install itself; no downstream build tooling is affected.

## Migration Plan

1. Update `pyproject.toml`: remove `build-system` section, keep `project` metadata, update `[tool.pytest.ini_options]` note (pytest.ini already uses INI keys).
2. Update `Makefile` to use `uv run ruff` and `uv run pytest`.
3. Update `AGENTS.md` "Running" section to document `uv` commands.
4. Recreate `.venv` using `uv venv`.
5. Verify with `uv pip install -e .` and `uv run pytest`.

## Open Questions

None. The change is straightforward and does not affect behavior.