## 1. Update CLI parser to accept `--storage` on each subcommand

- [x] 1.1 Add `--storage` argument to the `add` subparser in `snekdo/__main__.py`
- [x] 1.2 Add `--storage` argument to the `list` subparser in `snekdo/__main__.py`
- [x] 1.3 Add `--storage` argument to the `complete` subparser in `snekdo/__main__.py`
- [x] 1.4 Add `--storage` argument to the `delete` subparser in `snekdo/__main__.py`
- [x] 1.5 Add `--storage` argument to the `modify` subparser in `snekdo/__main__.py`
- [x] 1.6 Add `--storage` argument to the `show` subparser in `snekdo/__main__.py`
- [x] 1.7 Keep `--storage` on the main parser for backward compatibility

## 2. Add tests for per-subcommand `--storage` usage

- [x] 2.1 Add test: `--storage` works after `list` subcommand
- [x] 2.2 Add test: `--storage` works after `add` subcommand
- [x] 2.3 Add test: `--storage` works after `complete` subcommand
- [x] 2.4 Add test: `--storage` works after `delete` subcommand
- [x] 2.5 Add test: `--storage` works after `modify` subcommand
- [x] 2.6 Add test: `--storage` works after `show` subcommand
- [x] 2.7 Add test: `--storage` still works before subcommand (backward compatibility)

## 3. Verify

- [x] 3.1 Run `pytest` to ensure all tests pass
- [x] 3.2 Manually verify `snekdo list --storage /tmp/todos.json` works
