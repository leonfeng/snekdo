## Why

The `add` and `modify` commands accept a `--due` date string without any validation. Users can accidentally enter invalid dates (e.g., "2024-13-45" or "not-a-date"), and the system silently stores garbage. This change adds validation to ensure due dates are well-formed and meaningful.

## What Changes

- Validate the `--due` date format when adding and modifying todo items
- Reject dates that are not in valid ISO 8601 format (YYYY-MM-DD)
- Reject dates that are in the past (before today's date)
- Display a clear error message when the due date is invalid
- Add a new `due-date-validation` capability with delta specs

## Capabilities

### New Capabilities
- `due-date-validation`: Validates due dates for the `add` and `modify` commands

### Modified Capabilities
- (none)

## Impact

- Affected code: `snekdo/__main__.py` (handle_add, handle_modify), `snekdo/models.py` (optional due date validation helper)
- Affected tests: `tests/test_cli.py` (add new validation tests, update existing tests that use invalid dates)
- No new dependencies
- No breaking changes to existing valid usage
