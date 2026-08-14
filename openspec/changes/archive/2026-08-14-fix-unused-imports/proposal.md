## Why

The codebase contains several unused imports across its Python source and test files. These unused imports add maintenance burden, can confuse readers about which dependencies are actually needed, and increase the risk of import-time side effects. Removing them is a clean, zero-behavior-change improvement.

## What Changes

- Remove all unused imports from Python files in `snekdo/` and `tests/`.
- No new capabilities, no modified capabilities, no behavior changes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. This is a pure code-quality refactor with no spec-level behavior changes.

## Impact

- Affected code: `snekdo/__main__.py`, `snekdo/models.py`, `snekdo/storage.py`, `tests/test_cli.py`, `tests/test_storage.py`.
- No API, dependency, or system changes.
- Tests should continue to pass without modification.
