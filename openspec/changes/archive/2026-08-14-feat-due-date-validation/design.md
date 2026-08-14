## Context

The `add` and `modify` commands in `snekdo/__main__.py` accept a `--due` string argument without any validation. The `Todo` model stores `due` as `Optional[str]` with no format constraints. This means invalid dates like "2024-13-45" or "not-a-date" are silently stored.

## Goals / Non-Goals

**Goals:**
- Add validation for the `--due` date format (YYYY-MM-DD) in both `add` and `modify` commands
- Reject dates that are in the past (before the current date)
- Display clear error messages when validation fails
- Prevent invalid dates from being stored

**Non-Goals:**
- No changes to the `Todo` model data structure
- No changes to storage format
- No changes to list/show commands (they display dates as-is)
- No timezone handling (dates are stored as plain strings)
- No date parsing beyond format validation

## Decisions

### Decision: Validate in the CLI layer, not the model

**Choice**: Perform date validation in `handle_add` and `handle_modify` in `snekdo/__main__.py`, not in the `Todo` model.

**Rationale**: 
- The model is a simple data class; validation is a CLI concern
- This keeps the model lightweight and the validation logic co-located with the CLI
- Easier to test since the validation is in the CLI functions

**Alternatives considered**:
- Validate in the model's `__post_init__` or a setter - but this would couple the model with validation logic
- Create a separate validation utility module - overkill for this simple change

### Decision: Use `datetime.strptime` for parsing

**Choice**: Use Python's standard library `datetime.strptime` with format `"%Y-%m-%d"` to validate the date format.

**Rationale**:
- Standard library only (no new dependencies)
- Simple and well-understood
- Raises `ValueError` on invalid format, which can be caught and converted to a user-friendly error

**Alternatives considered**:
- Use `datetime.fromisoformat` - but this accepts more formats than just YYYY-MM-DD
- Use regex - less robust than strptime

### Decision: Reject past dates

**Choice**: Compare the parsed date against the current date (`datetime.now().date()`). Reject if the due date is before today.

**Rationale**:
- A due date in the past is likely a mistake
- This is a common expectation for todo apps
- The spec explicitly requires this

**Alternatives considered**:
- Allow past dates with a warning - but this could lead to confusion
- Allow past dates without warning - but this doesn't solve the problem

### Decision: Empty/None due dates are allowed

**Choice**: If `--due` is not provided or is an empty string, treat it as no due date (None).

**Rationale**:
- Many todos don't have due dates
- This is consistent with the existing behavior
- The spec explicitly requires this

## Risks / Trade-offs

### Risk: Existing tests with invalid dates may fail

**Impact**: Low - some existing tests may use invalid dates like "2024-13-45" which would now be rejected.

**Mitigation**: Update existing tests to use valid dates.

### Risk: Users may be confused by the new validation

**Impact**: Low - the error messages will be clear.

**Mitigation**: Clear error messages explaining the expected format and why the date is rejected.

### Risk: Date validation may be too strict

**Impact**: Low - the format is standard and well-understood.

**Mitigation**: The validation uses standard `datetime.strptime` which is well-tested.

## Migration Plan

This is a behavior change that adds validation. No data migration is required.

## Open Questions

None - the implementation approach is clear.
