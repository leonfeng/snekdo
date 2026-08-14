## Context

The `--debug` flag is defined in `snekdo/__main__.py` line 48:

```python
parser.add_argument("--debug", action="store_true", help="Print debug information")
```

However, `args.debug` is never read anywhere in the codebase. The flag is purely cosmetic — it accepts the argument but produces no behavior. The previous `fix-storage-flag-placement` change explicitly excluded modifying `--debug`.

## Goals / Non-Goals

**Goals:**
- Make `--debug` functional by printing debug information to stderr when set.
- Debug output should include the command being executed and the effective storage path.
- Keep debug output separate from stdout so it doesn't interfere with piping.

**Non-Goals:**
- Do not change the behavior of any other flag or command.
- Do not add verbose/trace-level logging beyond the debug flag.
- Do not change the storage flag or other arguments.

## Decisions

### Decision: Print debug info in `handle_command()`

**Rationale**: `handle_command()` is the central dispatch point for all subcommands. Adding debug output here ensures every command emits debug info consistently, without duplicating code in each handler.

**Implementation**:
- In `handle_command()`, check `if args.debug:` before dispatching.
- Print debug messages to stderr using `print(..., file=sys.stderr)`.
- Include the command name and the effective storage path.

### Decision: Use `print(..., file=sys.stderr)` for debug output

**Rationale**: Debug output should not pollute stdout, which users may pipe to other commands or files. Using stderr keeps debug output separate.

### Decision: Storage path resolution

**Rationale**: The effective storage path is determined by `args.storage` if provided, otherwise the default `~/.snekdo/todos.json`. We can compute this in `handle_command()` or within each handler. To keep it simple and consistent, we'll resolve it in `handle_command()` by checking `args.storage` and falling back to the default path.

## Implementation Plan

1. Add a helper function `_get_storage_path(args)` that returns the effective storage path.
2. In `handle_command()`, add debug output before dispatching:
   - Print `DEBUG: command=<command>` to stderr.
   - Print `DEBUG: storage_path=<path>` to stderr.
3. Ensure the existing `--debug` argument remains unchanged.
4. Add tests for the debug flag behavior.

## Risks / Trade-offs

- **Risk**: Debug output could break tests that capture stdout if debug is accidentally enabled.
  **Mitigation**: Debug output goes to stderr, and tests should not enable `--debug` unless testing it.
- **Risk**: Storage path resolution might differ from the actual path used by each handler.
  **Mitigation**: The path resolution logic mirrors `TodoStorage.__init__()`.

## Migration Plan

No migration needed. The change is purely additive — existing usage continues to work, and `--debug` now produces output instead of being a no-op.