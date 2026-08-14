## Context

`snekdo/__main__.py` imports `datetime` at module level (line 8) and again inside `validate_due_date()` (line 31). The local import is redundant because the module-level import already binds `datetime` in the function's global scope.

## Goals / Non-Goals

**Goals:**
- Remove the redundant local `from datetime import datetime` inside `validate_due_date()` to eliminate the duplicate import.

**Non-Goals:**
- No behavior changes, no new features, no refactoring beyond the redundant import removal.

## Decisions

- Simply delete the redundant `from datetime import datetime` line inside `validate_due_date()`. The module-level import on line 8 is sufficient and already in scope.

## Risks / Trade-offs

- This is a safe, no-op cleanup. No risk of behavior change.

## Migration Plan

- No migration needed. The fix is a single-line removal.

## Open Questions

- None.