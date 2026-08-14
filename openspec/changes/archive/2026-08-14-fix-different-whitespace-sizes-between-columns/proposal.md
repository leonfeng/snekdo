## Why

The `list` command renders a fixed-width table where each column uses a fixed format width (e.g. `{Status:<10}`, `{Priority:<10}`, `{Due:<15}`, `{Created At:<25}`). The separator between columns is a single space, but because the column widths are fixed, the visual whitespace between columns appears inconsistent — especially when content is shorter than the allocated width, leaving large gaps, or when dynamic columns (ID, Title) are narrower than their fixed counterparts. This fix makes the whitespace between columns uniform by computing column widths from content and using consistent separators.

## What Changes

- Compute the ID and Title column widths dynamically from the actual content (already partially done), but also make the fixed-width columns (Status, Priority, Due, Created At) adapt to their actual content width so that the whitespace between columns is uniform.
- Update the `handle_list` function in `snekdo/__main__.py` to format the table with consistent column spacing.
- Add/update tests to verify uniform column spacing.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `list-display`: Add a requirement that column whitespace is uniform and consistent across the list output table.

## Impact

- Affected code: `snekdo/__main__.py` (`handle_list` function), `tests/test_cli.py`
- No new dependencies or API changes.
