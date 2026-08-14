## Why

The `list` command formats the ID column with a fixed width of 35 characters (`{'ID':<35}`), but nanoid-generated IDs are only 21 characters long. This leaves a large gap of extra whitespace between the ID and Title columns, making the table output unnecessarily wide and harder to read.

## What Changes

- Make the ID column width dynamic, computed from the longest actual ID in the current list (mirroring the existing dynamic Title column width logic).
- Cap the ID column width at a reasonable maximum to prevent extremely long IDs from breaking the layout.
- Update the list output formatting in `snekdo/__main__.py` so both the header and data rows use the computed ID width.
- Update the test helper `_parse_list_line` in `tests/test_cli.py` to parse the dynamic ID column width instead of assuming a fixed 35-character width.

## Capabilities

### Modified Capabilities

- `list-display`: The list output display currently uses a fixed ID column width; this change makes the ID column width dynamic based on the longest ID in the list.

## Impact

- `snekdo/__main__.py`: `handle_list` function's table formatting logic.
- `tests/test_cli.py`: `_parse_list_line` helper and any tests that assert exact column positions.
