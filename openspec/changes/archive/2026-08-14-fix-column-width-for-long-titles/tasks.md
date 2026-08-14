## 1. Update list-display spec

- [x] 1.1 Add delta spec file at `openspec/changes/fix-column-width-for-long-titles/specs/list-display/spec.md` covering adaptive Title column width and ellipsis truncation.

## 2. Implement dynamic column width in handle_list

- [x] 2.1 Compute the required Title column width from the longest title in the current todo list, capped at a maximum width (e.g., 40 characters).
- [x] 2.2 Truncate titles that exceed the maximum width with an ellipsis (`...`).
- [x] 2.3 Update the table header and row formatting to use the dynamic Title width while keeping other column widths fixed.

## 3. Update tests

- [x] 3.1 Add or update tests to verify that long titles are displayed fully (without truncation) when they fit within the maximum width.
- [x] 3.2 Add or update tests to verify that titles exceeding the maximum width are truncated with an ellipsis.
- [x] 3.3 Update any existing tests that assert the exact total line width of 125 characters.

## 4. Verify

- [x] 4.1 Run the test suite to confirm all tests pass.
