## Context

`UserStorage.delete_user(user_id)` currently only removes the user record, leaving the user's todos in the todo storage. The API and web layers work around this by calling `TodoStorage.delete_all_user_todos(user_id)` before `UserStorage.delete_user(user_id)`. This scatters the account-deletion contract across multiple classes.

## Goals / Non-Goals

**Goals:**
- Add a single `UserStorage.delete_user_with_todos(user_id, todo_storage)` method that removes both the user's todos and the user record.
- Update the API and web account-deletion handlers to use the new method.
- Add tests for the new method and cascading deletion behavior.

**Non-Goals:**
- Do not change the existing `delete_user` or `delete_all_user_todos` methods.
- Do not change authentication, JWT token invalidation, or web UI templates.
- Do not add new dependencies.

## Decisions

### Decision 1: New method signature

Use `delete_user_with_todos(self, user_id: str, todo_storage: TodoStorage) -> bool` as the method signature. The `TodoStorage` instance is passed as a parameter because `UserStorage` and `TodoStorage` are separate classes. This keeps the method testable and avoids circular imports.

**Alternative considered:** Embed `TodoStorage` as a dependency in `UserStorage.__init__`. Rejected because it would couple the two classes and make `UserStorage` harder to instantiate in tests.

### Decision 2: Order of operations

Delete todos first, then the user record. This ensures that if the todo deletion fails, the user record is preserved for investigation.

**Alternative considered:** Delete the user first, then the todos. Rejected because orphaned todos would exist briefly if the todo deletion fails.

### Decision 3: Return value

Return `True` if the user was found and deleted, `False` otherwise. This is consistent with `UserStorage.delete_user` and `TodoStorage.delete_all_user_todos` (which always returns `None`).

### Decision 4: Update API and web handlers

Replace the two-line pattern:
```python
todo_storage.delete_all_user_todos(user_id)
user_storage.delete_user(user_id)
```
with:
```python
user_storage.delete_user_with_todos(user_id, todo_storage)
```

## Risks / Trade-offs

- **Risk:** Existing code that calls `delete_user` directly (outside the API/web handlers) will not cascade delete. **Mitigation:** The new method is the preferred API; documentation should encourage its use. Existing `delete_user` behavior is preserved for backward compatibility.
- **Risk:** The `todo_storage` parameter is required, so callers must always pass it. **Mitigation:** This is explicit and testable.

## Migration Plan

1. Add `delete_user_with_todos` to `UserStorage`.
2. Update `api.py` and `web.py` to use the new method.
3. Add tests in `test_storage.py` and `test_api.py`.
4. Run the full test suite to verify no regressions.

## Open Questions

None.