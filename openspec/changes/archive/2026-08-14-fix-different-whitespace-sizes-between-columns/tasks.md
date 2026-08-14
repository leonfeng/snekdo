## 1. Update list-display spec

- [x] 1.1 Add delta spec file at `openspec/changes/fix-different-whitespace-sizes-between-columns/specs/list-display/spec.md` covering uniform column whitespace.

## 2. Implement uniform column whitespace in handle_list

- [x] 2.1 Ensure the list output uses a single space separator between all columns.
- [x] 2.2 Compute dynamic column widths (ID, Title) from content, capped at maximums.
- [x] 2.3 Keep fixed column widths (Status: 10, Priority: 10, Due: 15, Created At: 25) and pad consistently.
- [x] 2.4 Ensure the table header and data rows use the same formatting.

## 3. Update tests

- [x] 3.1 Add a test verifying uniform whitespace between columns in the list output.
- [x] 3.2 Add a test verifying that the table header aligns with data rows.
- [x] 3.3 Update any existing tests that assert exact output line widths.

## 4. Verify

- [x] 4.1 Run the test suite to confirm all tests pass.
