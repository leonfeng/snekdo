## 1. Model + JSON persistence

- [x] 1.1 Add `tags: list[str]` (default `[]`) and `category: str | None` (default `None`) to `Todo` dataclass in `snekdo/models.py`
- [x] 1.2 Extend `Todo.to_dict()` to include `tags` and `category`
- [x] 1.3 Extend `Todo.from_dict()` to load `tags` (default `[]`) and `category` (default `None`, empty string → `None`)
- [x] 1.4 Model tests: defaults, round-trip, backward-compatible loading from old-format JSON (missing keys)

## 2. Storage

- [x] 2.1 Extend `TodoStorage.modify()` (JSON path) in `snekdo/storage.py` to accept and apply `tags` and `category` kwargs
- [x] 2.2 Add `tags` (TEXT, JSON-encoded) and `category` (TEXT) columns to the SQLite schema in `snekdo/storage_sqlite.py`, with an in-place `ALTER TABLE` migration guarded by a column-exists check
- [x] 2.3 Update all `TodoStorageSQLite` CRUD paths (add/get/load/save/modify) to read and write `tags` and `category`
- [x] 2.4 Ensure recurrence in `snekdo/storage.py` (JSON) and `snekdo/storage_sqlite.py` copies `tags` and `category` to the next occurrence
- [x] 2.5 Storage tests (JSON + SQLite): persistence round-trip, modify tags/category, SQLite migration on a pre-existing DB, recurrence copying tags/category
