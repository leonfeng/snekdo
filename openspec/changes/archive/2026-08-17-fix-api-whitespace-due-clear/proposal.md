## Why

`modify_todo` in `snekdo/api.py` checks `if update_data.due:` before validating
and applying the due-date update. A whitespace-only string like `"   "` is
truthy, so the code enters the block, calls `validate_due_date("   ")` which
returns `None` (after stripping), and sets `update_dict["due"] = None`. This
clears the existing due date instead of treating the whitespace as "not
provided".

## What Changes

- Change the due-check in `modify_todo` to also reject whitespace-only strings:
  `if update_data.due is not None and update_data.due.strip() != "":`.
- Update the `api-due-date-completed` OpenSpec capability to explicitly cover
  whitespace-only due values.

## Capabilities

### Modified Capabilities

- `api-due-date-completed`: Extend the "PUT with empty string due preserves
  existing due date" scenario to also cover whitespace-only strings.

## Impact

- **Affected code**: `snekdo/api.py` (`modify_todo`).
- **No new dependencies**.
- **Compatibility**: Whitespace-only due values now preserve the existing due
  date instead of clearing it.
