## Why

The CLI `modify` command currently lacks a `--completed` flag, so users cannot toggle the completed status of a todo through the command line. The API (`TodoUpdate` model) and storage layer (`storage.modify()`) already support updating the `completed` field, but the CLI surface is missing this capability.

## What Changes

- Add a `--completed` argument to the `modify` subparser in `snekdo/__main__.py`.
- Update `handle_modify()` to include `completed` in the "no fields to update" check and build the update dict when `--completed` is provided.
- Update the `todo-modification` spec to include the completed field as a modifiable attribute.
- Add/update tests to cover the new `--completed` behavior.

## Capabilities

### Modified Capabilities

- `todo-modification`: Add `--completed` as a modifiable field in the modify command.

## Impact

- Affected code: `snekdo/__main__.py` (parser and `handle_modify`), `openspec/specs/todo-modification/spec.md`, `tests/test_cli.py`.
- No new dependencies.
- No breaking changes.
