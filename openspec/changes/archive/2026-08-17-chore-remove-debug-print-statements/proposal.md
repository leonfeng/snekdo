## Why

Debug print statements (literal `print(...)` calls with a `DEBUG:` prefix) are leftover
development artifacts in the codebase. One such print in `snekdo/web.py` is always emitted
(every profile update), which is a bug and a potential data leak. The remaining ones in
`snekdo/__main__.py` are gated behind the `--debug` flag but use raw `print()` instead of
the project's existing `logging` infrastructure (already used in `snekdo/storage.py`).

## What Changes

- Remove the always-on debug print in `snekdo/web.py` (line ~337, profile update handler).
- Replace the `--debug` `print()` statements in `snekdo/__main__.py` with `logger.debug()`
  calls using the existing `logging` module, so debug information is still emitted to
  stderr when `--debug` is set but through proper logging infrastructure.
- Configure the logging level to `DEBUG` when `--debug` is enabled so the messages are
  actually emitted.
- Keep the emitted text format identical (`DEBUG: command=...`, `DEBUG: storage_path=...`)
  so existing tests continue to pass without modification.
- No spec-level behavior change: the `--debug` flag is still accepted and still produces
  debug output on stderr; only the implementation mechanism changes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None (no requirement-level changes). The existing `debug-flag` capability's requirements
continue to hold; only the implementation mechanism changes.

## Impact

- `snekdo/__main__.py` — debug print statements replaced with logging.
- `snekdo/web.py` — always-on debug print removed.
- `tests/test_cli.py` — no changes needed (output format preserved).
- `openspec/specs/debug-flag/spec.md` — no changes needed (behavior preserved).
