## Why

The E2E test helper function `_row()` in `tests/e2e/test_todos.py` returns a coroutine instead of a Playwright Locator because `.first` is not awaited. This causes `AttributeError: 'coroutine' object has no attribute 'locator'` in 7 test functions when they try to chain `.locator("td").first.inner_text()` on the result.

## What Changes

- Fix `_row()` function to properly await `.first`, returning a resolved Locator instead of a coroutine
- This enables 7 test functions to work correctly: test_edit_todo, test_edit_todo_empty_title, test_complete_todo, test_complete_todo_redirect, test_delete_todo, test_delete_todo_redirect, test_show_todo

## Capabilities

### New Capabilities

- `e2e/test-todos`: Fix test helper `_row()` coroutine issue in tests/e2e/test_todos.py

### Modified Capabilities

- (none - no existing spec requirements changing)

## Impact

- 7 E2E tests in `tests/e2e/test_todos.py` will pass
- No API or implementation changes needed - pure test helper fix
