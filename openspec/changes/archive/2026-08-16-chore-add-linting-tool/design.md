## Context

The `snekdo` project is a Python CLI todo manager with a `snekdo/` package and `tests/`. It uses setuptools for packaging, pytest for tests, and has no linting tool currently. The project context specifies Python 3.11+, standard library only for the CLI, and `pytest.ini` must use INI `[pytest]` keys.

## Goals / Non-Goals

**Goals:**
- Add `ruff` as a development dependency for fast Python linting and formatting.
- Configure ruff rules in `pyproject.toml` covering PEP 8, unused imports, and common pitfalls.
- Provide a convenient lint command for developers.

**Non-Goals:**
- No changes to the runtime behavior of the `snekdo` package.
- No new features or user-facing changes.
- No migration of existing code style beyond what ruff enforces.

## Decisions

- **Ruff over flake8/black/isort**: Ruff is a single fast tool that replaces flake8, black, and isort, reducing tooling complexity. It is the modern standard for Python linting.
- **Ruleset**: Use `PYI`, `UP`, `RUF`, `F`, `E`, `W`, `I` rules with a reasonable subset. Start with `ruff check` (no auto-format) to avoid large formatting diffs, then enable formatting in a follow-up.
- **Dev dependency placement**: Add ruff under `[project.optional-dependencies]` as `dev` so it does not affect runtime installs.

## Risks / Trade-offs

- **Existing code may violate rules**: Running ruff on the full codebase may reveal violations. Mitigation: run `ruff check` first, fix violations incrementally, and keep the lint command as a non-blocking dev tool.
- **Formatter changes**: Enabling `ruff format` will reformat the entire codebase. Mitigation: separate from linting; format only after confirming rules pass.

## Migration Plan

1. Add ruff to `pyproject.toml` under optional dependencies and `[tool.ruff]`.
2. Run `ruff check .` to identify violations.
3. Fix any violations in the codebase.
4. Run `ruff format .` if formatting is enabled.
5. Verify with `ruff check .` again.

## Open Questions

- Which specific ruff rules to enable? Default PEP 8 + common rules is a reasonable starting point.
- Should `ruff format` be enabled immediately or only `ruff check`? Starting with `check` only reduces initial diff size.
