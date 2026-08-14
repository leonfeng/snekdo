## Why

The list and show commands display the status of pending todos as a blank space (`" "`) instead of the word "pending". This makes the status column ambiguous and inconsistent with the completed status which shows a checkmark. Users cannot visually distinguish pending items by their status label in the list view.

## What Changes

- Modify the status display in `handle_list` so that pending todos show "pending" instead of a blank space.
- Modify the status display in `handle_show` so that pending todos show "pending" instead of a blank space.
- Update the `list-display` and `todo-show` delta specs to reflect the new expected behavior.

## Capabilities

### Modified Capabilities

- `list-display`: The Status column should display "pending" for pending todos (currently displays a blank space) and "✓" for completed todos.
- `todo-show`: The Status field should display "pending" for pending todos (currently displays a blank space) and "✓" for completed todos.

## Impact

- Affected code: `snekdo/__main__.py` (`handle_list` and `handle_show` functions).
- Affected specs: `openspec/specs/list-display/spec.md`, `openspec/specs/todo-show/spec.md`.
- Tests: `tests/test_cli.py` may need updates to reflect the new status strings.
