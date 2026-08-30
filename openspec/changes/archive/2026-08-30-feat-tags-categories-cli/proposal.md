# Proposal: Tags & Categories — CLI

## Why

The model and storage layers now support `tags` and `category`. This slice exposes them through the CLI: `--tag`/`--category` flags on `add` and `modify`, filter flags on `list`, and new columns in list output.

## What Changes

- `add` gains `--tag` (repeatable) and `--category`.
- `modify` gains `--tag` (repeatable) and `--category` (empty string clears).
- `list` gains `--tag` and `--category` filter flags.
- List output gains `Tags` (comma-joined, capped 30) and `Category` columns after `Created At`.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `list-display`: new `Tags` and `Category` columns; `--tag` and `--category` filter flags.
- `todo-modification`: `modify` gains `--tag` (repeatable) and `--category` flags.

## Impact

- `snekdo/__main__.py`: `create_parser()`, `handle_add`, `handle_modify`, `handle_list`.
- Tests: `tests/test_cli.py`.
