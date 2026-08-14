## Why

Users currently have no control over the order in which todos appear when listing. The default behavior (newest first) is not always the most useful, and users need the ability to sort by different criteria to better organize their workflow.

## What Changes

- Add `--sort` flag to the `list` command with multiple sort options
- Add `--reverse` flag to reverse the sort order
- Update list output to reflect sorted results
- Add tests for sorting functionality

## Capabilities

### New Capabilities

- `todo-sorting`: Define sorting behavior for todo list output including sort field, sort direction, and edge cases

### Modified Capabilities

- `todo-priority`: Update to support sorting by priority level

## Impact

- **Code**: `snekdo/__main__.py` (handle_list function), `snekdo/models.py` (may need sort key methods)
- **Tests**: New test cases in `tests/test_cli.py` for sorting functionality
- **CLI**: New command-line arguments for `list` command
- **Backward compatibility**: Default behavior remains unchanged (newest first) when no sort flags are provided
