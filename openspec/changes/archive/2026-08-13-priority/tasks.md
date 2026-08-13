## 1. Add Priority Model

- [x] 1.1 Add `Priority` enum to `snekdo/models.py` with values `low`, `medium`, `high`
- [x] 1.2 Add `priority` field to `Todo` dataclass with default value "medium"
- [x] 1.3 Update `to_dict()` to include priority
- [x] 1.4 Update `from_dict()` to handle missing priority (backward compatibility)
- [x] 1.5 Run tests to verify model changes

## 2. Add Priority Storage Support

- [x] 2.1 Add `filter_by_priority()` method to `TodoStorage` in `snekdo/storage.py`
- [x] 2.2 Add `modify_priority()` method to `TodoStorage`
- [x] 2.3 Add tests for storage methods in `tests/test_storage.py`

## 3. Add Priority to CLI

- [x] 3.1 Add `--priority` argument to `add` command in `snekdo/__main__.py`
- [x] 3.2 Add `--priority` argument to `list` command in `snekdo/__main__.py`
- [x] 3.3 Add `--priority` argument to `modify` command in `snekdo/__main__.py`
- [x] 3.4 Update list output formatting to show priority column
- [x] 3.5 Add tests for CLI commands in `tests/test_cli.py`

## 4. Validation and Error Handling

- [x] 4.1 Add validation for priority values (low, medium, high) in CLI
- [x] 4.2 Add error handling for invalid priority values
- [x] 4.3 Add tests for validation and error cases

## 5. Testing and Verification

- [x] 5.1 Run full test suite to verify all tests pass
- [x] 5.2 Test end-to-end: add, list, modify with priority
- [x] 5.3 Test backward compatibility with existing todos
