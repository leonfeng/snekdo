## Design

### Problem
The CLI `modify` command in `snekdo/__main__.py` does not expose the `completed` field, even though:
- `Todo.__post_init__` / `to_dict` / `from_dict` handle `completed` correctly.
- `TodoStorage.modify()` accepts `completed` in `**kwargs` and updates `todo.completed`.
- The API `TodoUpdate` Pydantic model includes `completed: bool | None = None`.
- The API `modify_todo` endpoint sets `update_dict["completed"] = update_data.completed` when provided.

### Approach
Add the `--completed` flag to the `modify` subparser and thread it through `handle_modify()`.

#### Parser change
In `create_parser()`, add after the `--priority` argument:
```python
modify_parser.add_argument(
    "--completed",
    type=str,
    choices=["true", "false"],
    default=None,
    help="Set the completed status (true or false)",
)
```

#### Handle change
In `handle_modify()`:
1. Add `args.completed is None` to the "no fields to update" check.
2. After the `priority` block, add:
```python
if args.completed is not None:
    update_data["completed"] = args.completed.lower() == "true"
```

### Tests
Add a test in `tests/test_cli.py` covering:
- `--completed true` sets `completed=True`.
- `--completed false` sets `completed=False`.
- The "no fields to update" error when only `todo_id` is provided.

### Spec
Update `openspec/specs/todo-modification/spec.md` to include `completed` as a modifiable field.
