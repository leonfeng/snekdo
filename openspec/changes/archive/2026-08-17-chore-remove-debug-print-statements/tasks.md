## 1. Replace debug prints with logging in CLI

- [x] 1.1 In `snekdo/__main__.py`, replace the two `print(f"DEBUG: ...", file=sys.stderr)`
  calls inside the `--debug` branch with `logger.debug(...)` calls using the standard
  `logging` module.
- [x] 1.2 In `snekdo/__main__.py`, configure the logging level to `DEBUG` and ensure a
  stderr handler is present when `args.debug` is True, before the debug messages are
  emitted.
- [x] 1.3 Keep the exact text format (`DEBUG: command=...`, `DEBUG: storage_path=...`)
  so existing `TestDebugFlag` assertions continue to pass.

## 2. Remove the always-on debug print in the web handler

- [x] 2.1 In `snekdo/web.py`, remove the `print(f"DEBUG: display_name=...")` line inside
  `update_profile()`.

## 3. Verify the change

- [x] 3.1 Run `uv run pytest tests/test_cli.py::TestDebugFlag` to confirm the existing
  debug-flag tests still pass.
- [x] 3.2 Run the full test suite `uv run pytest` to confirm no regressions.
