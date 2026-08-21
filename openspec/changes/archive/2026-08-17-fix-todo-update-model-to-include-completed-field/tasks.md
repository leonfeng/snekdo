## 1. Add `--completed` argument to modify parser

- [x] 1.1 Add `--completed` argument to the `modify_parser` subparser in `snekdo/__main__.py`

## 2. Update `handle_modify` to handle `--completed`

- [x] 2.1 Add `args.completed is None` to the "no fields to update" validation
- [x] 2.2 Add logic to convert `args.completed` to boolean and include in update dict

## 3. Update spec

- [x] 3.1 Update `openspec/specs/todo-modification/spec.md` with completed scenarios

## 4. Add tests

- [x] 4.1 Add tests for `--completed true` and `--completed false` in `tests/test_cli.py`

## 5. Verify

- [x] 5.1 Run `uv run pytest` to ensure all tests pass
