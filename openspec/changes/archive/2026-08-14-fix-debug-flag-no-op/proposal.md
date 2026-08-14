## Why

The `--debug` flag is declared on the CLI parser in `snekdo/__main__.py` but is never consumed by any handler, making it a no-op. Users who pass `--debug` expect to see debug information about the command being executed, but currently receive nothing. This change makes the flag functional so that debug output is emitted when requested.

## What Changes

- Implement the `--debug` flag so that when it is passed, the CLI emits debug information to stderr.
- Debug output will include the command being executed and the effective storage path, helping users diagnose CLI behavior.
- No changes to existing command behavior when `--debug` is omitted.

## Capabilities

### New Capabilities

- `debug-flag`: Defines the expected behavior of the `--debug` flag, ensuring it prints debug information (command name, storage path) to stderr when set.

### Modified Capabilities

<!-- None — no existing spec-level behavior is changed beyond adding the new debug capability. -->

## Impact

- Affected code: `snekdo/__main__.py` (parser and command handlers).
- No changes to `snekdo/models.py` or `snekdo/storage.py`.
- No new dependencies.
- Existing tests continue to pass; the `--debug` flag is additive.