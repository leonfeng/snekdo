## Why

The web frontend (`snekdo/web.py`) validated due dates by importing `validate_due_date`
from `snekdo.__main__`, but `__main__.py` imports `snekdo.web` at the top level. This
creates a circular import: `__main__` → `web` → `__main__`. Moving the shared
due-date validation function into a new standalone module `snekdo/due_date.py`
eliminates the cycle and gives both the CLI and web layers a single source of truth.

## What Changes

- Create `snekdo/due_date.py` with a public `validate_due_date()` function.
- Remove the local `validate_due_date` definition from `snekdo/__main__.py` and
  import it from `snekdo.due_date`.
- Remove the private `_validate_due_date` helper from `snekdo/api.py` and import
  `validate_due_date` from `snekdo.due_date`.
- Remove the `_validate_due_date` helper from `snekdo/web.py` and import
  `validate_due_date` from `snekdo.due_date`.
- No behavior change: validation rules, error messages, and return values are
  preserved.

## Capabilities

No capabilities are added or modified. This is a pure refactor; no spec-level
behavior changes.

## Impact

- Affected code: `snekdo/due_date.py` (new), `snekdo/__main__.py`, `snekdo/api.py`,
  `snekdo/web.py`.
- No new dependencies.
- No API or CLI behavior changes.
