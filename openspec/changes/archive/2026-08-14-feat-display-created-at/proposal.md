## Why

The `list` command currently displays ID, Title, Status, Priority, and Due, but omits the creation date. Users need to see when each todo was created to better understand the order and timing of their tasks.

## What Changes

- Add a `Created At` column to the `list` command output table
- Display the `created_at` value (ISO 8601 format) for each todo
- Align the new column with the existing table layout
- Add tests verifying the created_at column is rendered

## Capabilities

### New Capabilities

- `list-display`: Define the list output display including the new created_at column

### Modified Capabilities

- (none)

## Impact

- **Code**: `snekdo/__main__.py` (handle_list function - update print header and row formatting)
- **Tests**: New test cases in `tests/test_cli.py` for the created_at column
- **CLI**: No new command-line arguments; output format change only
- **Backward compatibility**: The list still works without the flag; only the output table gains a column
