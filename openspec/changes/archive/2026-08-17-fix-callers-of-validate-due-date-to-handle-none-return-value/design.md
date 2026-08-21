## Context

`validate_due_date()` in `snekdo.due_date` returns `str | None` — it returns `None` for empty or `None` input. The web edit form in `snekdo/web.py` calls `validate_due_date(due)` and unconditionally passes the result to `storage.modify()`. Because the form field defaults to `""`, every edit submission produces `None` from `validate_due_date`, which `storage.modify()` treats as "clear the due date", silently wiping the existing due date.

## Goals / Non-Goals

**Goals:**
- Fix the web edit form to preserve the existing due date when the user submits without changing it.
- Make CLI and API modify handlers consistent with the intended behavior: empty string clears the field, omitting the field leaves it unchanged.

**Non-Goals:**
- Do not change `validate_due_date()` itself (it correctly returns `None` for empty input).
- Do not change the `Todo` model or storage layer.
- Do not add new dependencies.

## Decisions

1. **Use truthy checks instead of `is not None` checks.** In `__main__.py` and `api.py`, the callers check `if args.due is not None` / `if update_data.due is not None`. But `""` is a valid value that should clear the field. Using `if args.due` (truthy) means empty strings are treated as "provided" (and thus clear the field), while `None` (omitted) is treated as "not provided" (leave unchanged). This is consistent with the existing convention that "empty string is a valid value (clears field)".

2. **In `web.py`, only pass `due` to `storage.modify()` when `due_clean` is not `None`.** This preserves the existing due date when the form field is left empty. If the user explicitly clears the field (empty string), `validate_due_date("")` returns `None`, and we should clear the due date. Wait — this is a subtlety. The form field default is `""`, so we can't distinguish between "not changed" and "explicitly cleared to empty". 

   Decision: Treat empty string in the form as "preserve existing due date". This is the most user-friendly behavior and matches the common case. If a user wants to clear the due date, they can use the CLI with `--due ""` (which would need a different approach). Actually, looking at the form, there's no way to distinguish. So the safest behavior is: if `due_clean is None`, don't pass `due` to `storage.modify()` at all, preserving the existing value.

   Actually, let me reconsider. The form field is `due: str | None = Form(default="")`. When the user leaves it empty, `due` is `""`. When the user clears it, `due` is also `""`. So we can't distinguish. The best behavior is to treat `""` as "preserve existing" in the web form.

3. **No change to `validate_due_date()`.** The helper correctly returns `None` for empty/None input. The bug is in the callers not handling this `None` correctly.

## Risks / Trade-offs

- **Risk**: Users who expect the web form to clear the due date when leaving it empty will be surprised. **Mitigation**: This is the correct and expected behavior — leaving a form field empty should not clear the existing value.
- **Risk**: The CLI `--due ""` behavior is unchanged — it still clears the field. This is consistent with the existing convention.

## Migration Plan

No migration needed. This is a bug fix that changes behavior to be correct.

## Open Questions

None.
