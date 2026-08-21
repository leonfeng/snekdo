## Tasks

- [x] Read `snekdo/__main__.py` and `snekdo/api_client.py` to understand the current sync and update_todo implementation.
- [x] Update `_sync()` in `snekdo/__main__.py` to pass the local todo's `completed` value when calling `client.update_todo()` during push/both sync.
- [x] Update `tests/test_cli.py` sync tests to verify the `completed` field is included in `update_todo` calls and that the server's `completed` status is correctly synced.
- [x] Update `tests/test_api_client.py` (if exists) to verify `update_todo` includes `completed` in the request body.
- [x] Run `pytest` to verify all tests pass.
- [x] Run `openspec status --change fix-api-client-update-todo-to-handle-completed-field` to verify the change is complete.