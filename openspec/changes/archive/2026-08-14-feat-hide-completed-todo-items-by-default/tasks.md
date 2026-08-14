## 1. Update list default status

- [x] 1.1 Change the default value of `--status` from `"all"` to `"pending"` in `snekdo/__main__.py`

## 2. Update tests

- [x] 2.1 Add test verifying completed items are hidden by default
- [x] 2.2 Add test verifying `--status all` still shows all items
- [x] 2.3 Update existing list tests that expect all items by default

## 3. Update documentation

- [x] 3.1 Update README.md to reflect the new default behavior

## 4. Verify

- [x] 4.1 Run `pytest` to ensure all tests pass
- [x] 4.2 Run `snekdo list` with sample data to verify the output
