## 1. Update list display formatting

- [x] 1.1 Compute dynamic ID column width in `handle_list` based on the longest ID (capped at 35), ensuring minimum width of "ID" header length
- [x] 1.2 Apply ID truncation with ellipsis for IDs exceeding the max width, reusing the existing truncation helper pattern
- [x] 1.3 Update the header and data row print statements to use the computed ID width

## 2. Update tests

- [x] 2.1 Update `_parse_list_line` in `tests/test_cli.py` to parse the dynamic ID column width instead of assuming a fixed 35-character width
- [x] 2.2 Add a test verifying that the ID column width is computed from the longest ID
- [x] 2.3 Add a test verifying that long IDs are truncated with an ellipsis

## 3. Verify

- [x] 3.1 Run `pytest` to confirm all tests pass
- [x] 3.2 Manually verify the list output with short and long IDs looks correct
