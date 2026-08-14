## Context

The `--storage` flag is defined on the main argparse parser in `snekdo/__main__.py`. In argparse, arguments defined on the parent parser become "global" options that must appear before the subcommand. The README documents `snekdo list --storage /path/to/todos.json`, which fails because `--storage` is parsed as an unrecognized argument for the `list` subparser.

## Goals / Non-Goals

**Goals:**
- Make `--storage` work in both positions: before the subcommand (global) and after the subcommand (per-subcommand).
- Maintain backward compatibility with existing usage.

**Non-Goals:**
- Do not change the behavior of the `--storage` flag once it is correctly positioned.
- Do not add new storage-related features (e.g., auto-detection, multiple storage files).
- Do not modify the `--debug` flag or other arguments.

## Decisions

### Decision: Add `--storage` to each subparser

**Rationale**: argparse does not support "global" arguments that work both before and after subcommands in a single definition. The standard approach is to add the argument to both the parent parser and each subparser.

**Alternatives considered**:
1. **Remove `--storage` from the main parser and add it only to subparsers**: This would break existing users who use `snekdo --storage X list`. Not chosen.
2. **Use a custom argparse action**: More complex, harder to maintain. Not chosen.
3. **Add `--storage` to both parent and subparsers**: Best approach — maintains backward compatibility while supporting the documented usage.

### Decision: Use identical `--storage` definition on all subparsers

Each subparser will get the same `--storage` argument definition as the main parser:
```python
parser.add_argument("--storage", help="Path to the storage file")
```

This ensures consistent behavior and documentation across all commands.

## Risks / Trade-offs

- **Risk**: Duplicating the `--storage` argument across 6 subparsers increases code duplication.
  **Mitigation**: The duplication is minimal and localized to the parser setup. A helper could be used, but it adds complexity for little benefit.
- **Risk**: Users might confuse which position to use.
  **Mitigation**: Both positions work, so this is resolved.

## Migration Plan

No migration needed. The change is backward compatible — existing usage continues to work, and the documented usage now also works.

## Open Questions

- Should the `--storage` flag also be available as a positional argument? No — it's an optional flag.
- Should the `--debug` flag be implemented as part of this change? No — it's a separate issue.
