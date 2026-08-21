## Context

`TodoCreate.priority` and `TodoUpdate.priority` in `snekdo/api.py` are plain
`str` Pydantic fields. Pydantic does not validate that the value is one of the
expected priority values (`low`, `medium`, `high`). The `Priority` enum in
`snekdo/models.py` exists but is not used in the API schemas.

## Goals / Non-Goals

**Goals:**
- Constrain `TodoCreate.priority` and `TodoUpdate.priority` to the enum values
  `["low", "medium", "high"]` using `Literal[...]`.
- Add API-level scenarios to the `todo-priority` OpenSpec capability.

**Non-Goals:**
- No changes to the `Priority` enum itself.
- No changes to the CLI (it already validates priority).

## Decisions

- **Decision**: Use `Literal["low", "medium", "high"]` for both schemas instead
  of `Field(enum=...)`.
  - **Rationale**: Pydantic v2 deprecates `Field(enum=...)` and treats it as an
    extra keyword argument that does not apply validation. `Literal` provides
    both JSON schema enum generation and actual data validation, returning a
    clear 422 error for invalid values.
  - **Alternative**: Use the `Priority` StrEnum directly. Rejected because the
    existing code uses plain `str` fields and we want minimal changes.
  - **Alternative**: Use `Annotated[str, Field(json_schema_extra={...})]`.
    Rejected because it only affects the JSON schema, not validation.

## Risks / Trade-offs

- **Risk**: Clients sending invalid priority values will now get 422 errors.
  - **Mitigation**: This is the intended behavior; the spec requires validation.

## Migration Plan

No migration needed. Invalid values were always invalid; this just enforces it.

## Open Questions

None.
