## Context

`modify_todo` in `snekdo/api.py` uses `if update_data.due:` to decide whether to
validate and apply a due-date update. The `validate_due_date()` function strips
whitespace and returns `None` for whitespace-only strings. So:

1. `{"due": "   "}` passes the truthiness check (`"   "` is truthy).
2. `validate_due_date("   ")` returns `None`.
3. `update_dict["due"] = None` is set, which clears the existing due date.

The fix is to check for both `None` and whitespace-only strings.

## Goals / Non-Goals

**Goals:**
- Change the due-check in `modify_todo` to `if update_data.due is not None and update_data.due.strip() != "":`.
- This makes whitespace-only due values behave like empty/missing due values,
  preserving the existing due date.
- Update the `api-due-date-completed` OpenSpec capability to cover whitespace.

**Non-Goals:**
- No changes to `validate_due_date()` itself (it already correctly strips and
  returns `None` for empty/whitespace).
- No changes to `TodoCreate` (which already handles empty due correctly via
  `validate_due_date`).

## Decisions

- **Decision**: Use `if update_data.due is not None and update_data.due.strip() != "":`.
  - **Rationale**: Matches the semantics of `validate_due_date()` (which treats
    whitespace-only as empty) and the OpenSpec "empty string is treated as not
    provided" rule.
  - **Alternative**: Use `if update_data.due:` only. Rejected because it does
    not handle whitespace-only strings.

## Risks / Trade-offs

- **Risk**: None. This is a bug fix that makes the API consistent with the spec
  and the CLI (`modify` already treats empty `--due` as "not provided").

## Migration Plan

No migration needed. This fixes incorrect behavior.

## Open Questions

None.
