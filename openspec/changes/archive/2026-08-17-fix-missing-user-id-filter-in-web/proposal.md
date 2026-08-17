## Why

The web frontend currently filters todos by the logged-in user's `user_id` but the `Todo` model's `to_dict()` serialization conditionally omits the `user_id` field when it is `None`. This means todos created through the CLI (which do not set `user_id`) are silently dropped from the web UI because the storage layer's `load(user_id=...)` filter compares `None` against the logged-in user's ID string and excludes them. Users who create todos via the CLI then switch to the web UI will see an incomplete or empty list, breaking the expected multi-interface consistency.

## What Changes

- Update `Todo.to_dict()` to always serialize the `user_id` field (including `None`), so the stored JSON faithfully records the association and the web UI can reliably filter by `user_id`.
- Ensure the web list endpoints consistently apply the `user_id` filter derived from the authenticated session, and that the CLI `add` command also sets `user_id` on created todos for consistency.
- Add/update tests to verify that todos created via one interface are visible in the other interface when the user is the same.

## Capabilities

### New Capabilities

- `web-user-id-filter`: Ensure the web frontend correctly filters and persists the `user_id` association for all todos, so the web UI and CLI share a consistent view of per-user todos.

### Modified Capabilities

- `htmx-jinja2-frontend`: Update the serialization and filtering behavior so the web UI always shows the authenticated user's todos regardless of how they were created.

## Impact

- Affected code: `snekdo/models.py` (`Todo.to_dict`), `snekdo/storage.py` (`TodoStorage.load`), `snekdo/web.py` (list endpoints), `snekdo/__main__.py` (`handle_add`).
- No API-level breaking changes; the JSON storage format gains a consistent `user_id` key for all todos.
- Tests in `tests/test_web.py` and `tests/test_cli.py` may need updates.