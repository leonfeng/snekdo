## 1. Setup dependencies

- [x] 1.1 Add `fastapi` and `uvicorn` to `pyproject.toml` (as `dependencies` or `[project.optional-dependencies]` with an `api` extra).
- [x] 1.2 Create `snekdo/api.py` module with the FastAPI app scaffold.

## 2. Implement the FastAPI backend

- [x] 2.1 Define Pydantic request/response models (`TodoCreate`, `TodoUpdate`, `TodoResponse`).
- [x] 2.2 Create the FastAPI app instance with a dependency-injected `TodoStorage`.
- [x] 2.3 Implement `GET /api/v1/health` endpoint.
- [x] 2.4 Implement `GET /api/v1/todos` endpoint (list all todos).
- [x] 2.5 Implement `GET /api/v1/todos/{todo_id}` endpoint (show one todo).
- [x] 2.6 Implement `POST /api/v1/todos` endpoint (add a todo).
- [x] 2.7 Implement `POST /api/v1/todos/{todo_id}/complete` endpoint.
- [x] 2.8 Implement `PUT /api/v1/todos/{todo_id}` endpoint (modify a todo).
- [x] 2.9 Implement `DELETE /api/v1/todos/{todo_id}` endpoint.
- [x] 2.10 Add error handling for 404 (not found) and 422 (validation error) responses.

## 3. Add the `serve` CLI subcommand

- [x] 3.1 Add a `serve` subparser to `create_parser()` in `snekdo/__main__.py`.
- [x] 3.2 Add `--host` and `--port` arguments to the `serve` subparser.
- [x] 3.3 Add `--storage` argument to the `serve` subparser.
- [x] 3.4 Implement `handle_serve()` to launch uvicorn with the FastAPI app.

## 4. Add tests

- [x] 4.1 Create `tests/test_api.py`.
- [x] 4.2 Add tests for the health endpoint.
- [x] 4.3 Add tests for CRUD endpoints using `TestClient`.
- [x] 4.4 Add a test for custom storage path via `--storage`.

## 5. Update documentation

- [x] 5.1 Update `README.md` to describe the `serve` command and API usage.
- [x] 5.2 Update `README.md` to mention the `fastapi`/`uvicorn` dependencies.
