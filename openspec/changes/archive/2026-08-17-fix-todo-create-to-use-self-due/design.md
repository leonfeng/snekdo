## Context

`TodoCreate.to_todo()` builds a `Todo` from raw request data without
validating `due`.  The API `add_todo` endpoint therefore validates the due
date *after* building the `Todo` and overrides `todo.due` — a redundant
two-step.  The shared `validate_due_date()` helper in `snekdo.due_date`
already returns `None` for empty/`None` input and raises `ValueError` for
invalid or past dates.

## Goals / Non-Goals

**Goals:**
- Make `TodoCreate.to_todo()` self-validating for the `due` field.
- Remove redundant validation/override in the API `add_todo` endpoint.
- Remove redundant validation in the web `add_todo` route.

**Non-Goals:**
- Do not change CLI `handle_add` (it constructs `Todo` directly).
- Do not change `TodoUpdate` / `modify_todo` (they already validate separately).
- Do not add new dependencies.

## Decisions

1. **Validate in `to_todo()` rather than at every call site.**
   `TodoCreate.to_todo()` is the single place that converts a create
   request into a `Todo`.  Validating there guarantees every `Todo`
   produced from this factory is valid, and callers (API, web) can rely
   on it without re-validating.

2. **Reuse `snekdo.due_date.validate_due_date`.**
   This helper already handles `None`, `""`, invalid format, and past
   dates with clear error messages.  No new validation code is needed.

3. **Propagate `ValueError` as 422 in the API.**
   The API `add_todo` endpoint wraps `to_todo()` in a `try/except ValueError`
   and returns `HTTPException(422, detail=...)`, matching existing behavior.

4. **Web route relies on `to_todo()` validation.**
   The web `add_todo` route calls `to_todo()` and catches `ValueError`,
   re-rendering the form with an error message.

## Risks / Trade-offs

- **Risk**: Callers that bypass `to_todo()` (e.g., direct `Todo()`
  construction) are unaffected.  **Mitigation**: `to_todo()` is the only
  factory method for create requests; direct `Todo()` construction is not
  used for incoming requests.
- **Risk**: Existing tests that mock `to_todo()` may need updating.
  **Mitigation**: Update affected tests to expect validated `Todo` objects.

## Migration Plan

No database or config migration needed.  The change is purely in the
request-to-model conversion layer.

## Open Questions

None.
