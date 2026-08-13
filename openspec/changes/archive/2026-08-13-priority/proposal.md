# Proposal: Add Priority Levels to Todo Items

## Why

Users need to express urgency and importance when creating todo items. Currently, todos have no notion of priority, making it impossible to distinguish between critical tasks and low-priority reminders. Adding priority levels gives users a quick visual cue for triage and helps them focus on what matters most.

## What Changes

- Add a `--priority` option to the `add` command with values: `low`, `medium`, `high`
- Add a `--priority` filter to the `list` command
- Add a `--priority` option to the `modify` command
- Display priority level in list output
- Store priority as a new required field on the `Todo` model
- Add tests for all new behavior

## Capabilities

### New Capabilities

- `todo-priority`: Add priority levels (low, medium, high) to todo items with filtering and display support

### Modified Capabilities

- `todo-modification`: Extend the modify command to support updating the priority field

## Impact

- **New files**: None (feature added to existing modules)
- **Modified files**:
  - `snekdo/models.py` — Add `priority` field to `Todo` model
  - `snekdo/__main__.py` — Add `--priority` argument to `add` and `list` commands, add `--priority` to `modify` command, update list output formatting
  - `tests/test_models.py` — Add tests for priority field
  - `tests/test_cli.py` — Add tests for priority CLI behavior
  - `tests/test_storage.py` — Add tests for priority storage behavior
- **Dependencies**: No new dependencies
- **Breaking changes**: None
