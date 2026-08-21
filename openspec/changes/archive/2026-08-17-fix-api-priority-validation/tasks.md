## 1. Add enum validation to API schemas

- [x] 1.1 Add `enum=["low", "medium", "high"]` to `TodoCreate.priority` in
          `snekdo/api.py`.
- [x] 1.2 Add `enum=["low", "medium", "high"]` to `TodoUpdate.priority` in
          `snekdo/api.py`.

## 2. Update OpenSpec capability

- [x] 2.1 Add a new requirement "Validate priority values via API" to
          `openspec/specs/todo-priority/spec.md`.
- [x] 2.2 Add scenario "Invalid priority value via API returns 422" covering
          `POST /api/v1/todos` and `PUT /api/v1/todos/{id}`.
- [x] 2.3 Add scenario "Empty priority value via API returns 422".

## 3. Verify

- [x] 3.1 Run `uv run pytest` to confirm existing tests still pass.
- [x] 3.2 Run a targeted TestClient check: `POST /api/v1/todos` with
          `{"priority": "urgent"}` should return 422.
