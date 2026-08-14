## 1. Add sort parameter to CLI

- [x] 1.1 Add `--sort` and `--reverse` arguments to the `list` subparser in `__main__.py`
- [x] 1.2 Add type validation for `--sort` (choices: created_at, title, priority, completed)
- [x] 1.3 Add type validation for `--reverse` (boolean flag)

## 2. Implement sorting logic

- [x] 2.1 Create helper function to map priority to sort key (high=3, medium=2, low=1)
- [x] 2.2 Implement sort key function for created_at (datetime comparison)
- [x] 2.3 Implement sort key function for title (string comparison)
- [x] 2.4 Implement sort key function for completed (boolean comparison)
- [x] 2.5 Apply sorting after filtering and before limiting in `handle_list()`

## 3. Add error handling

- [x] 3.1 Validate sort field parameter and return error for invalid values
- [x] 3.2 Handle None/empty values consistently for each sort field
- [x] 3.3 Ensure error messages are user-friendly

## 4. Write tests

- [x] 4.1 Add test for sorting by created_at (newest first)
- [x] 4.2 Add test for sorting by created_at reversed (oldest first)
- [x] 4.3 Add test for sorting by title (alphabetical)
- [x] 4.4 Add test for sorting by title reversed (reverse alphabetical)
- [x] 4.5 Add test for sorting by priority (high to low)
- [x] 4.6 Add test for sorting by priority reversed (low to high)
- [x] 4.7 Add test for sorting by completed status
- [x] 4.8 Add test for sorting with limit applied
- [x] 4.9 Add test for sorting with filters applied
- [x] 4.10 Add test for invalid sort field error handling
- [x] 4.11 Add test for empty list sorting

## 5. Documentation and cleanup

- [x] 5.1 Update README.md to document new flags
- [x] 5.2 Run all tests to verify no regressions
- [x] 5.3 Run linter to ensure code quality
