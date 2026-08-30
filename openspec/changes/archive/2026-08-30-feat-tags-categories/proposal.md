# Proposal: Tags and Categories

## Why

snekdo todos currently carry only `priority` and `due` as organizing attributes. Users have no way to group related todos (e.g. "work", "home", "urgent") or to filter by a free-form label. Tags are the minimal, highest-value organizational primitive: they unlock filtering, grouping, and future features (kanban boards, per-tag stats) without imposing a rigid hierarchy.

## What Changes

- **New `tags` field on `Todo`**: a list of strings, defaulting to an empty list. Serialized/deserialized through JSON with backward-compatible defaults.
- **New `category` field on `Todo`**: a single optional string, defaulting to `None`. A todo belongs to at most one category at a time (unlike tags, which are many-to-many).
- **CLI `add` and `modify`**: new `--tag` (repeatable) and `--category` flags. `add` accepts one or more `--tag` values; `modify` sets the full tag list (replacing existing) and optionally sets or clears `category`.
- **CLI `list`**: new `--tag` and `--category` filter flags. `--tag` accepts a single tag name; a todo matches if it contains that tag. Multiple tags cannot be combined in a single `list` invocation (OR semantics would require a new flag shape, deferred).
- **REST API**: `TodoCreate` and `TodoUpdate` gain `tags: list[str]` and `category: str | None`. `TodoResponse` includes both. `GET /api/v1/todos` gains optional `tag` and `category` query parameters for filtering.
- **Web UI**: the add and edit forms gain a tag input (comma-separated) and a category input. The list view shows tags and category as additional columns.
- **Storage**: both JSON and SQLite backends persist `tags` and `category`. The SQLite schema migrates in place (ALTER TABLE ADD COLUMN) so existing databases work without data loss.
- **Sync**: `ServerHttpClient` and the sync logic carry `tags` and `category` in create/update payloads so they round-trip through `snekdo sync`.
- **Display**: CLI list output gains a `Tags` column (comma-separated, truncated) and a `Category` column. Column widths follow the existing dynamic-width rules.

No breaking changes. Existing todos without `tags` or `category` load with empty list / `None` respectively.

## Capabilities

### New Capabilities

- `todo-tags`: tag and category fields on the Todo model — storage, serialization, CLI flags, API fields, and web form inputs.

### Modified Capabilities

- `list-display`: new `Tags` and `Category` columns in the CLI list output, plus `--tag` and `--category` filter flags.
- `todo-modification`: `modify` command gains `--tag` (repeatable) and `--category` flags.
- `fastapi-backend`: `TodoCreate`/`TodoUpdate`/`TodoResponse` models gain `tags` and `category`; `GET /api/v1/todos` gains `tag` and `category` query parameters.

## Impact

- `snekdo/models.py`: `Todo` dataclass gains `tags: list[str]` and `category: str | None`; `to_dict`/`from_dict` updated.
- `snekdo/storage.py`: JSON path unchanged (model handles it); `modify()` kwargs extended.
- `snekdo/storage_sqlite.py`: schema migration to add `tags` (TEXT, JSON-encoded) and `category` (TEXT) columns; all CRUD paths updated.
- `snekdo/__main__.py`: `create_parser` gains flags; `handle_add`, `handle_list`, `handle_modify` updated.
- `snekdo/api.py`: Pydantic models updated; list endpoint gains query params; response mapping updated.
- `snekdo/api_client.py`: sync payloads include `tags` and `category`.
- `snekdo/web.py` + templates: add/edit/list forms and rows updated.
- Tests: model, storage (JSON + SQLite), CLI, API, sync, and web e2e.
