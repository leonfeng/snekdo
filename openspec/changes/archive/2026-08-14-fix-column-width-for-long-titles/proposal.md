## Why

The `list` command uses fixed-width columns for the title and other fields. When a todo title exceeds the allocated width (30 characters for Title), it is silently truncated in the output, making it impossible to read the full title without opening the item details.

## What Changes

- Modify the list output formatting so that the Title column expands to fit the longest title, while keeping a reasonable maximum width and wrapping/truncating with an ellipsis only when necessary.
- Add a spec requirement covering title truncation behavior in the `list-display` capability.
- Update the `handle_list` function in `snekdo/__main__.py` to compute dynamic column widths based on actual content.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `list-display`: Add a requirement that the Title column must not truncate titles that fit within the display width, and define behavior for titles that exceed the maximum column width (ellipsis truncation).

## Impact

- Affected code: `snekdo/__main__.py` (`handle_list` function), `openspec/specs/list-display/spec.md`
- No new dependencies or API changes.
