## 1. Fix the due-check in `modify_todo`

- [x] 1.1 Change `if update_data.due:` to
          `if update_data.due is not None and update_data.due.strip() != "":`
          in `snekdo/api.py` (`modify_todo`).

## 2. Update OpenSpec capability

- [x] 2.1 Update the `api-due-date-completed` capability to extend the
          "PUT with empty string due preserves existing due date" scenario to
          also cover whitespace-only strings (e.g., `{"due": "   "}`).

## 3. Verify

- [x] 3.1 Run `uv run pytest` to confirm existing tests still pass.
- [x] 3.2 Run a targeted TestClient check: create a todo with a due date, then
          `PUT /api/v1/todos/{id}` with `{"due": "   "}` should preserve the
          existing due date.
