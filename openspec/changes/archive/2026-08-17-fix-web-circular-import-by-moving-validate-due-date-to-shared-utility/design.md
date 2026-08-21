## Context

`snekdo/web.py` defines a private `_validate_due_date()` that imports
`validate_due_date` from `snekdo.__main__`. But `__main__.py` imports
`register_web_routes` from `snekdo.web` at the top level, creating a circular
import: `__main__` → `web` → `__main__`. This breaks any code path that imports
both the CLI and the web module (e.g., `snekdo serve`).

## Goals / Non-Goals

**Goals:**
- Break the circular import by extracting `validate_due_date` into its own
  module (`snekdo/due_date.py`) that has no dependencies on the rest of the
  package.
- Update all callers (`__main__.py`, `api.py`, `web.py`) to import from the
  shared module.

**Non-Goals:**
- No change to validation rules, error messages, or return values.
- No new dependencies.
- No changes to the public API or CLI behavior.

## Decisions

1. **Create `snekdo/due_date.py` as a standalone utility module.**
   - The module imports only `datetime` from the standard library.
   - It exports a single public function `validate_due_date()`.
   - This module has no imports from `snekdo.*`, so it cannot participate in a
     circular import.

2. **Rename `_validate_due_date` → `validate_due_date` in `api.py`.**
   - `api.py` previously had a private `_validate_due_date`. Now it imports the
     public `validate_due_date` from `due_date.py`.
   - Behavior is preserved: empty/None → `None`, invalid format → `ValueError`,
     past date → `ValueError`.

3. **Rename `_validate_due_date` → `validate_due_date` in `web.py`.**
   - `web.py` previously imported from `__main__`. Now it imports from
     `due_date.py`.
   - The `TodoCreate` import from `api.py` is retained (used for the add route).

4. **Preserve `validate_due_date` return type.**
   - The function returns `str | None`: `None` for empty/None input, the
     validated date string otherwise. This matches the current behavior after
     the `Todo.from_dict` empty-string normalization.

## Risks / Trade-offs

- **Risk**: Importing `snekdo.due_date` from `snekdo.__main__` adds a new
  dependency, but since `due_date.py` is dependency-free, this cannot create a
  cycle.
- **Risk**: Existing tests that reference `_validate_due_date` (if any) must be
  updated. No such tests exist in the current codebase.
- **Trade-off**: The shared module is minimal; no attempt is made to add
  additional date utilities that might be needed in the future.

## Migration Plan

1. Create `snekdo/due_date.py` with the validation function.
2. Update `snekdo/__main__.py`: remove local `validate_due_date`, add
   `from snekdo.due_date import validate_due_date`.
3. Update `snekdo/api.py`: remove `_validate_due_date`, add
   `from snekdo.due_date import validate_due_date`.
4. Update `snekdo/web.py`: remove `_validate_due_date`, add
   `from snekdo.due_date import validate_due_date`.
5. Verify `snekdo serve` starts without import errors.
6. Run the test suite to confirm no regressions.

## Open Questions

None. The fix is straightforward and preserves all existing behavior.
