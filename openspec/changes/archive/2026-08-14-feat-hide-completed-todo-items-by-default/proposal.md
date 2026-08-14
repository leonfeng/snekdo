## Why

The `list` command currently shows all todos by default, including completed ones. Users often want to focus on pending tasks, so hiding completed items by default would reduce noise and improve the user experience.

## What Changes

- Change the default behavior of the `list` command to hide completed todo items
- Users can still view completed items using the `--status all` or `--status completed` flags
- Update existing tests and documentation to reflect the new default behavior

## Capabilities

### New Capabilities

- `list-default-filter`: Define the default filtering behavior for the list command, including hiding completed items by default

### Modified Capabilities

- (none)

## Impact

- **Code**: `snekdo/__main__.py` (handle_list function - change default status filter)
- **Tests**: Update existing list tests to account for the new default behavior
- **CLI**: No new command-line arguments; default output changes
- **Documentation**: README.md updated to reflect the new default behavior
- **Backward compatibility**: The `--status all` flag still shows all todos; only the default changes
