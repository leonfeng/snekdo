## Why

`validate_due_date()` in `snekdo/__main__.py` re-imports `datetime` inside the function body, even though `datetime` is already imported at the module level. This redundant import is a code-quality issue (redundant local import) that clutters the function and can trigger lint warnings.

## What Changes

- Remove the redundant `from datetime import datetime` inside `validate_due_date()` so the module-level import is used.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- None

## Impact

- Affected code: `snekdo/__main__.py` — `validate_due_date()` function.
- No behavior change; no API or dependency changes.