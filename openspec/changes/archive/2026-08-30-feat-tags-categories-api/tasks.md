## 1. Pydantic models

- [x] 1.1 Add `tags: list[str] = []` and `category: str | None = None` to `TodoCreate` in `snekdo/api.py`
- [x] 1.2 Add `tags: list[str] | None = None` and `category: str | None = None` to `TodoUpdate` in `snekdo/api.py`
- [x] 1.3 Add `tags: list[str]` and `category: str | None` to `TodoResponse` and update `from_todo()`

## 2. API handlers

- [x] 2.1 Update `POST /api/v1/todos` handler to pass `tags` and `category` from `TodoCreate` into the `Todo` object
- [x] 2.2 Update `PUT /api/v1/todos/{id}` handler to apply `tags` (full replace) and `category` (None clears) from `TodoUpdate`
- [x] 2.3 Add optional `tag` and `category` query parameters to `GET /api/v1/todos`; filter results after loading

## 3. Tests

- [x] 3.1 API tests: POST with tags and category returns them in response
- [x] 3.2 API tests: PUT with tags replaces list; PUT with category=None clears
- [x] 3.3 API tests: GET /todos?tag=... and ?category=... filter correctly
- [x] 3.4 API tests: TodoResponse includes tags and category for all endpoints
