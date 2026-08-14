## Why

The `list` command's `--sort` flag accepts invalid sort field values silently: when an unknown sort field is provided, `handle_list` falls back to sorting by `created_at` instead of rejecting the input with an error message and a non-zero exit code. This contradicts the existing `todo-sorting` specification, which requires invalid sort fields to be handled gracefully with an error.

## What Changes

- Modify `handle_list` in `snekdo/__main__.py` to validate the `--sort` value against the allowed sort fields and return a non-zero exit code with an error message when an invalid value is provided.
- Add a test in `tests/test_cli.py` covering the invalid sort field scenario.
- Add a delta spec to `openspec/changes/fix-handle-list-not-rejecting-invalid-sort-fields/specs/todo-sorting/spec.md` documenting the invalid-sort-field requirement change.

## Capabilities

### Modified Capabilities

- `todo-sorting`: The existing requirement "Handle invalid sort field" is being strengthened from a silent fallback to an explicit error rejection.

## Impact

- Affected code: `snekdo/__main__.py` (`handle_list`), `tests/test_cli.py`
- No API or dependency changes.
- Behavior change: `snekdo list --sort <invalid>` will now return exit code 1 with an error message instead of silently sorting by `created_at`.
