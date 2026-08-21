## Context

The project already uses Python's standard `logging` module (see `snekdo/storage.py`).
The CLI entry point (`snekdo/__main__.py`) currently uses raw `print(...)` calls with a
`DEBUG:` prefix for debug output, and `snekdo/web.py` has an always-on debug print that
emits user data on every profile update.

## Goals / Non-Goals

**Goals:**
- Eliminate all literal `print()` debug statements from the source code.
- Route debug output through the standard `logging` module.
- Preserve the existing `--debug` flag behavior: debug messages still appear on stderr
  when `--debug` is set, with the same text format so existing tests pass unchanged.
- Remove the always-on debug print in the web profile handler.

**Non-Goals:**
- Do not add new logging statements beyond replacing the existing debug prints.
- Do not change the `--debug` flag semantics or the `debug-flag` spec requirements.
- Do not modify unrelated code paths.

## Decisions

### Decision 1: Replace `print()` with `logger.debug()`

Use the existing `logging` module (already imported in `snekdo/storage.py`) rather than
adding a new dependency or a custom logging wrapper. In `snekdo/__main__.py`, obtain a
logger via `logging.getLogger(__name__)` and call `.debug()` for the command and storage
path messages.

### Decision 2: Configure logging level when `--debug` is set

When `args.debug` is True, set the root logger (or the snekdo package logger) level to
`logging.DEBUG` and ensure a stderr handler exists. This keeps debug output on stderr,
matching the current `print(..., file=sys.stderr)` behavior and the existing tests that
assert `DEBUG:` appears in `captured.err`.

### Decision 3: Preserve output format

Keep the exact text format (`DEBUG: command=<cmd>`, `DEBUG: storage_path=<path>`) so the
existing `TestDebugFlag` test assertions continue to pass without modification.

### Decision 4: Remove the always-on web.py print

The print in `snekdo/web.py` `update_profile()` is not gated by any flag and emits
`display_name` and `email`. It should be removed entirely.

## Risks / Trade-offs

- **Risk**: Logging may not be configured before `handle_command` runs, causing no output.
  **Mitigation**: Configure logging inline in `handle_command` when `--debug` is set,
  before the debug messages are emitted.
- **Risk**: Tests that mock `TodoStorage` may interfere with logging.
  **Mitigation**: Logging is independent of `TodoStorage`; the mock does not affect it.
- **Risk**: The `--debug` flag becomes a no-op if logging is not configured correctly.
  **Mitigation**: Verify with the existing `TestDebugFlag` test suite.

## Migration Plan

1. Edit `snekdo/__main__.py`: replace the two `print(f"DEBUG: ...", file=sys.stderr)`
   lines with `logger.debug(...)` calls and add logging configuration in the `--debug`
   branch.
2. Edit `snekdo/web.py`: remove the always-on `print(f"DEBUG: ...")` line.
3. Run `uv run pytest tests/test_cli.py::TestDebugFlag` to verify the existing tests pass.

## Open Questions

None. The approach is straightforward: replace debug prints with logging and remove the
always-on debug print.
