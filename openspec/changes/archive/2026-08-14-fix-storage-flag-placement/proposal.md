## Why

The `--storage` flag is documented in the README as `snekdo list --storage /path/to/todos.json`, but argparse treats it as a global option that must appear before the subcommand (`snekdo --storage /path/to/todos.json list`). This inconsistency breaks the documented workflow and forces users to remember a non-obvious argument order.

## What Changes

- Make the `--storage` flag work both before and after the subcommand for all CLI commands (add, list, complete, delete, modify, show).
- Update the `--storage` argument to be available on each subparser so users can place it where they expect it.
- Add tests verifying the `--storage` flag works after the subcommand.

## Capabilities

### New Capabilities

- `storage-flag`: Define the expected behavior of the `--storage` flag, including that it must be accepted in both global and per-subcommand positions.

### Modified Capabilities

<!-- None — no existing spec-level requirements are changing; this is a new capability covering a gap. -->

## Impact

- Affected code: `snekdo/__main__.py` (argparse parser setup), `tests/test_cli.py` (new tests).
- No changes to `snekdo/models.py` or `snekdo/storage.py`.
- No breaking changes — existing usage (`snekdo --storage X list`) continues to work.
