# Tasks: Recurring Todos

- [x] 1. Add `Repeat` enum (none|daily|weekly|monthly|yearly) and `repeat` +
  `last_completed_at` fields to `Todo` in `snekdo/models.py`; update
  `to_dict`/`from_dict` with backward-compatible defaults.
- [x] 2. Implement `next_due_date(due, repeat, now)` in `snekdo/models.py`
  with day-of-month and leap-year clamping; add unit tests in
  `tests/test_models.py`.
- [x] 3. Update `TodoStorage.complete_todo` to set `last_completed_at` and
  append a new pending occurrence when `repeat != "none"` (atomic within the
  existing file lock); add unit tests in `tests/test_storage.py`.
- [x] 4. Add `--repeat` choice flag to the `add` CLI subcommand and wire it
  into `handle_add`; add unit tests in `tests/test_cli.py`.
- [x] 5. Show a repeat tag in `handle_list` output for recurring todos; update
  any list-display tests in `tests/test_cli.py`.
- [x] 6. Add `repeat` to `TodoCreate`/`TodoUpdate`/`TodoResponse` in
  `snekdo/api.py` with validation; ensure complete endpoint triggers
  recurrence; add API tests in `tests/test_api.py`.
- [x] 7. Add a repeat selector to the web add-todo form and a repeat indicator
  in the todo list template; add/extend e2e coverage in `tests/e2e/`.
- [x] 8. Run full test suite (`uv run pytest`) and `openspec validate
  "feat-recurring-todos"`; update this file's checkboxes as each task lands.
