## 1. Storage Layer

- [x] 1.1 Add `modify()` method to `TodoStorage` class in `storage.py`
- [x] 1.2 Add tests for `modify()` method in `test_storage.py`

## 2. CLI Layer

- [x] 2.1 Add `modify` subparser to `__main__.py` with `--title`, `--description`, and `--due` arguments
- [x] 2.2 Implement `handle_modify()` function in `__main__.py`
- [x] 2.3 Add error handling for non-existent todos
- [x] 2.4 Add tests for modify command in `test_cli.py`

## 3. Integration & Testing

- [x] 3.1 Run full test suite to ensure no regressions
- [x] 3.2 Test edge cases: empty strings, invalid dates, missing required args
