## Why

Users currently have no way to view the full details of a single todo item. The `list` command shows a summary table, but users need a dedicated view that displays all fields of a todo (including description, created_at, and completion status) when they want to inspect a specific item.

## What Changes

- Add a new `show` command to the CLI that displays all details of a todo item by ID
- Display all fields: ID, Title, Description, Due, Priority, Status/Completed, Created At
- Add tests for the new command
- Update README to document the new command

## Capabilities

### New Capabilities

- `todo-show`: Define the behavior for displaying detailed information of a single todo item by ID

### Modified Capabilities

- (none)

## Impact

- **Code**: `snekdo/__main__.py` (new `handle_show` function and `show` subparser)
- **Tests**: New test cases in `tests/test_cli.py` for the show command
- **CLI**: New `snekdo show <todo-id>` command
- **Documentation**: README.md updated with the new command
- **Backward compatibility**: No changes to existing commands
