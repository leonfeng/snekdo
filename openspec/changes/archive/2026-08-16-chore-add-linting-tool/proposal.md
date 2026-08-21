## Why

The project currently has no linting tool, which means code style inconsistencies, potential bugs, and unused imports are not caught automatically. Adding a linting tool will enforce consistent code quality and help catch issues early in the development workflow.

## What Changes

- Add `ruff` as a development dependency for linting and formatting.
- Configure ruff rules in `pyproject.toml` following PEP 8 and common Python best practices.
- Add a `lint` command (via `make lint` or `pip run ruff`) so developers can run the linter.
- No changes to the runtime behavior of the `snekdo` package.

## Capabilities

No new or modified capabilities. This is a pure tooling change that does not alter externally observable behavior. `skip_specs: true` is set in `.openspec.yaml`.

## Impact

- `pyproject.toml`: add ruff as optional dev dependency and configuration.
- `pytest.ini` or `Makefile`: add lint target.
- Developer workflow: `ruff check` / `ruff format` can be run on the codebase.
