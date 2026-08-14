## 1. Update sorting logic in `handle_list`

- [x] 1.1 Import `datetime` (already imported) and add a helper to parse `created_at` strings
- [x] 1.2 Modify the `created_at` sort branch in `handle_list` to convert strings to `datetime` objects before sorting
- [x] 1.3 Handle empty/missing `created_at` values by treating them as earliest (epoch)

## 2. Add tests for datetime-based sorting

- [x] 2.1 Add a test verifying correct chronological order with microsecond-precision `created_at` values
- [x] 2.2 Add a test verifying reverse chronological order
- [x] 2.3 Add a test verifying empty `created_at` values sort consistently
- [x] 2.4 Add a test verifying mixed-precision ISO 8601 values sort correctly

## 3. Run existing tests to ensure no regressions

- [x] 3.1 Run `pytest` to verify all existing tests pass
- [x] 3.2 Verify the existing `test_list_sort_by_created_at` test still passes
