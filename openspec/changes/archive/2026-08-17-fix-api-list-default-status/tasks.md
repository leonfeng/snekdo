## 1. Update `list_todos` default status

- [x] 1.1 Change `status: str | None = Query(default=None, enum=[...])` to
       `status: str = Query(default="pending", enum=["all", "pending", "completed"])`
       in `snekdo/api.py`.
- [x] 1.2 Update the `if status == "pending"` / `elif status == "completed"` logic
       to also handle the new default (no change needed since default is "pending").

## 2. Update OpenSpec capability

- [x] 2.1 Add a new requirement "List todos defaults to pending" to
          `openspec/specs/fastapi-backend/spec.md`.
- [x] 2.2 Add a scenario "List todos defaults to pending filter" verifying that
          completed todos are excluded by default.

## 3. Verify

- [x] 3.1 Run `uv run pytest` to confirm existing tests still pass.
- [x] 3.2 Run a targeted TestClient check: create a pending and a completed todo,
          then `GET /api/v1/todos` should return only the pending one.
