## Tasks

- [x] 1. Add a helper function `_get_storage_path(args)` in `snekdo/__main__.py` that returns the effective storage path (from `args.storage` or the default `~/.snekdo/todos.json`).
- [x] 2. Modify `handle_command()` to print debug output to stderr when `args.debug` is True, including the command name and effective storage path.
- [x] 3. Add tests in `tests/test_cli.py` for the debug flag behavior:
  - [x] 3a. Test that `--debug` is accepted without error.
  - [x] 3b. Test that debug output is printed to stderr.
  - [x] 3c. Test that debug output includes the command name.
  - [x] 3d. Test that debug output includes the storage path.
  - [x] 3e. Test that debug output is suppressed when `--debug` is not set.
- [x] 4. Run the test suite to verify all tests pass.