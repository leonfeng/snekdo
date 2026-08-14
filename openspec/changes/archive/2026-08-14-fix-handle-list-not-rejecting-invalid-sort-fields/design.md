## Context

The `list` command already defines valid sort fields via argparse's `choices` parameter, which rejects invalid values at the CLI level. However, `handle_list` contains an `else` branch that silently defaults to `created_at` sorting when `args.sort` is not one of the four known fields. This means the function is not robust when called directly (e.g., from tests with mocked args) or if the argparse choices are ever bypassed.

## Goals / Non-Goals

**Goals:**
- Make `handle_list` validate the sort field explicitly and return exit code 1 with an error message when an invalid value is provided.
- Add a test covering the invalid sort field scenario.

**Non-Goals:**
- Changing the set of valid sort fields.
- Changing how sorting works for valid fields.
- Adding new sort fields.

## Decisions

### Decision: Validate sort field in `handle_list`

Instead of relying solely on argparse's `choices` (which only protects the CLI path), add an explicit validation check in `handle_list` that compares `args.sort` against the allowed set `{"created_at", "title", "priority", "completed"}`. If invalid, print an error message to stderr listing the valid fields and return 1.

Rationale: This makes the function robust to direct calls with mocked args (as in the test suite) and aligns the implementation with the existing spec requirement.

### Decision: Error message includes valid fields

The error message will list the valid sort fields (`created_at`, `title`, `priority`, `completed`) so the user knows what values are accepted.

## Risks / Trade-offs

- **Risk**: Existing tests that mock args with an invalid `sort` value might now fail with a different result. **Mitigation**: Add/adjust the test to expect the error.
- **Risk**: No impact on valid sort field behavior since the check only adds a new error path.

## Migration Plan

No migration needed. This is a bug fix that changes behavior only for invalid input that should have been rejected in the first place.

## Open Questions

None.
