## Context

See proposal.md for motivation. The `Todo` dataclass in `snekdo/models.py` is the single source of truth, persisted by `TodoStorage` (JSON) and `TodoStorageSQLite` (SQLite). The CLI in `snekdo/__main__.py` builds argparse subcommands and dispatches to `handle_*` functions. The FastAPI app in `snekdo/api.py` uses Pydantic models `TodoCreate`/`TodoUpdate`/`TodoResponse` and a `get_todos` handler with query-param filtering. The web layer in `snekdo/web.py` renders Jinja2 templates with HTMX.

The existing pattern for adding fields is: add to `Todo` dataclass with a default, extend `to_dict`/`from_dict`, add CLI flags + handler logic, extend Pydantic models, and update templates. `user_id` and `repeat` are precedent.

## Goals / Non-Goals

**Goals:**
- Add `tags: list[str]` and `category: str | None` to `Todo` with backward-compatible defaults.
- Expose via CLI (`add`, `modify`, `list --tag`, `list --category`), REST API (create/modify/list + query params), and web UI (add/edit/list).
- Persist in both JSON and SQLite backends; SQLite migrates in place.
- Round-trip through `snekdo sync`.

**Non-Goals:**
- No multi-tag OR filtering in a single invocation.
- No tag/category management subcommands.
- No hierarchical categories.
- No web UI beyond add/edit/list forms and columns.

## Decisions

1. **Tags serialized as a JSON array in SQLite TEXT column.** SQLite lacks native array type; JSON serialization mirrors the JSON backend and keeps a single representation. Alternatives: a `todo_tags` join table (rejected — overkill, adds FK + query complexity).

2. **Category is a single nullable string, not a list.** One category per todo keeps the model simple and matches a "folder" mental model. No normalization.

3. **`modify` replaces the full tag list.** Passing `--tag` sets the entire list (no append). Consistent with other `modify` flags (set-to-value semantics). Documented in the spec.

4. **Empty `--category ""` clears the field** (sets to `None`), matching the existing treatment of empty strings for nullable fields.

5. **API filters via query params** `tag` and `category` on `GET /api/v1/todos`, mirroring the CLI list flags.

6. **Web tag input is comma-separated** in a single text field; parsed by splitting on comma, trimming, and dropping empties. Avoids a custom tag widget.

7. **Column order in CLI list output:** existing columns keep their positions; `Tags` is inserted after `Created At` and `Category` after `Tags`, both dynamic-width (capped 30), single-space separators.

## Risks / Trade-offs

- [SQLite migration on existing DBs] → Guard `ALTER TABLE ... ADD COLUMN` with a column-exists check; run at schema init. Test migration on a pre-existing DB.
- [Tags as JSON in SQLite means full scans for tag filters] → Acceptable at personal-list scale; document as a trade-off.
- [Backward-compatible loading] → `from_dict` defaults `tags` to `[]` and `category` to `None`; test old-format JSON.
- [Comma-separated tag parsing edge cases] → Trim whitespace, drop empty tokens, dedupe while preserving order.

## Migration Plan

- **JSON backend:** no migration. Old files lack the keys; `from_dict` supplies defaults.
- **SQLite backend:** on init, if `tags`/`category` columns are missing, run `ALTER TABLE todos ADD COLUMN tags TEXT DEFAULT '[]'` and `ALTER TABLE todos ADD COLUMN category TEXT`.
- **Rollback:** drop the two SQLite columns and revert model/CLI/API/template changes; old code ignores the new JSON keys.

## Open Questions

- None that block the specs or task breakdown; all decisions above are settled.
