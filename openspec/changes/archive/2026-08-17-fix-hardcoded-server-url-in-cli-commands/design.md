## Context

The CLI already has a `--server` flag on `sync`, `register`, and `login`, but `profile`, `profile-update`, `change-password`, and `delete-account` hardcode `http://127.0.0.1:8000` in their `ServerHttpClient` construction. The fix is localized to `snekdo/__main__.py`.

## Goals / Non-Goals

**Goals:**
- Add `--server` to the four affected CLI subcommand parsers with the same default as the existing commands.
- Update the four handlers to use `args.server` instead of the hardcoded URL.
- Ensure the existing `--storage` behavior is preserved.

**Non-Goals:**
- No changes to the API, models, storage, or `ServerHttpClient` itself.
- No changes to the web frontend or e2e tests (they exercise the server, not the CLI).
- No changes to `sync`, `register`, or `login` behavior beyond consistency.

## Decisions

- **Decision**: Use the same `--server` argument definition as `sync`/`register`/`login` (`default="http://127.0.0.1:8000"`, `help="Server base URL"`).
  - **Rationale**: Consistency with existing commands; users already expect this pattern.
  - **Alternative**: A top-level `--server` flag. Rejected because the existing commands use per-subparser flags, and a top-level flag would be more invasive.
- **Decision**: Place the `--server` argument after `--storage` in the parser definitions (or before, matching existing commands).
  - **Rationale**: Consistency with `sync`/`register`/`login` which place `--server` before `--storage`.

## Risks / Trade-offs

- **Risk**: Adding `--server` to the parsers changes the `--help` output and the set of recognized arguments.
  - **Mitigation**: This is the intended behavior; existing tests that check help should be updated if any exist.
- **Risk**: If a handler references `args.server` but the parser doesn't add the argument, `AttributeError` occurs.
  - **Mitigation**: Add the argument and update the handler in the same change.

## Migration Plan

No migration needed. The default behavior is identical; only the set of accepted flags changes.

## Open Questions

None. The fix is straightforward and consistent with existing patterns.