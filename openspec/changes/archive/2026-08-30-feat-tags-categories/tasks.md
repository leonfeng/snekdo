## 1. Model

- [ ] 1.1 Add `tags: list[str]` (default `[]`) and `category: str | None` (default `None`) to the `Todo` dataclass in `snekdo/models.py`.
- [ ] 1.2 Extend `Todo.to_dict()` to serialize `tags` and `category`; extend `Todo.from_dict()` to load them with backward-compatible defaults (`tags=[]`, `category=None` when keys are missing).

## 2. Storage

- [ ] 2.1 Extend `TodoStorage.modify()` (JSON path) in `snekdo/storage.py` to accept and apply `tags` and `category` kwargs.
- [ ] 2.2 Add `tags` (TEXT, JSON) and `category` (TEXT) columns to the SQLite schema in `snekdo/storage_sqlite.py`, with an in-place `ALTER TABLE` migration guarded by a column-exists check for existing databases.
- [ ] 2.3 Update all `TodoStorageSQLite` CRUD paths (add/get/load/save/modify) to read and write `tags` and `category`.
- [ ] 2.4 Ensure a recurring todo's next occurrence (created on completion) copies `tags` and `category` from the source.

## 3. CLI

- [ ] 3.1 Add `--tag` (repeatable, default `[]`) and `--category` (default `None`) flags to the `add` subparser in `snekdo/__main__.py`; pass them to `Todo` in `handle_add`.
- [ ] 3.2 Add `--tag` (repeatable) and `--category` flags to the `modify` subparser; in `handle_modify`, pass `tags` (replacing the list when any `--tag` given) and `category` (empty string clears it) to `storage.modify`.
- [ ] 3.3 Add `--tag` and `--category` filter flags to the `list` subparser; filter in `handle_list` (tag: contained in `todo.tags`; category: exact match) before sorting/limiting.
- [ ] 3.4 Add `Tags` and `Category` columns to the CLI list output after `Created At` (dynamic width, cap 30, single-space separators); tags joined by `", "`.

## 4. REST API

- [ ] 4.1 Add `tags: list[str] = []` and `category: str | None = None` to `TodoCreate` and `TodoUpdate`; add both to `TodoResponse` and `TodoResponse.from_todo()` in `snekdo/api.py`.
- [ ] 4.2 Apply `tags`/`category` in the `POST /api/v1/todos` and `PUT /api/v1/todos/{id}` handlers; on PUT, `tags` replaces the list and `category=None` clears it.
- [ ] 4.3 Add optional `tag` and `category` query parameters to `GET /api/v1/todos`; filter the result set (tag contained, category exact) alongside the existing status/priority filters.

## 5. Sync

- [ ] 5.1 Carry `tags` and `category` in `ServerHttpClient` create/update payloads so they round-trip through `snekdo sync`.

## 6. Web UI

- [ ] 6.1 Add a comma-separated tags text input and a category text input to the web add and edit forms in `snekdo/web.py` + templates.
- [ ] 6.2 Parse the comma-separated tags input (split, trim, drop empties) and the category value in the web add/edit handlers, storing them on the todo.
- [ ] 6.3 Display `Tags` and `Category` columns in the web list view.

## 7. Tests

- [ ] 7.1 Model tests: defaults, round-trip, and backward-compatible loading from old-format JSON (missing keys).
- [ ] 7.2 Storage tests (JSON + SQLite): persistence, modify, SQLite migration on a pre-existing DB, and recurrence copying tags/category.
- [ ] 7.3 CLI tests: add/modify/list flags, list filters, and new list columns.
- [ ] 7.4 API tests: create/modify with tags+category, list `tag`/`category` query filters, and `TodoResponse` inclusion.
- [ ] 7.5 Web tests: add/edit form inputs and list columns.
