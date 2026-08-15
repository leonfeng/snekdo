## Why

The project currently uses `setuptools` as its build backend, which is slower and less modern than `uv`. Switching to `uv` as the build tool will speed up installation, improve reproducibility, and align with current Python packaging best practices.

## What Changes

- Replace the `setuptools`-based `pyproject.toml` build configuration with a `uv`-compatible configuration.
- Update the `Makefile` and `AGENTS.md` "Running" instructions to use `uv` commands (`uv pip install`, `uv run`, etc.) instead of `pip install`.
- Remove `setuptools` from dependencies and build-system requirements.
- Keep all existing functionality, dependencies, and behavior unchanged.

## Capabilities

No new or modified capabilities are introduced. This is a pure tooling change with no spec-level behavior changes. `skip_specs: true` is set in `.openspec.yaml`.

## Impact

- Affected code: `pyproject.toml`, `Makefile`, `AGENTS.md`, `.venv` (recreated by uv).
- Affected dependencies: build tooling changes from `setuptools` to `uv`; runtime dependencies remain the same.
- No API or behavior changes.