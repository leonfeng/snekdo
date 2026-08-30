## Context

See proposal for motivation. The `Todo` model and both storage backends (JSON + SQLite) already persist `tags` and `category` (delivered by the model and storage slices). This slice wires them through `snekdo/__main__.py`.

## Goals / Non-Goals

**Goals:**
- Expose `--tag` (repeatable) and `--category` on `add` and `modify`.
- Expose `--tag` and `--category` as filters on `list`.
- Show `Tags` and `Category` columns in list output.

**Non-Goals:**
- No changes to model, storage, API, or web in this slice.

## Decisions

1. **`--tag` is repeatable (`action="append"`, default `None` → treated as empty).** On `add`, the list of tags is passed directly to `Todo(tags=...)`. On `modify`, if any `--tag` was given, the full list replaces the existing tags; if none given, tags are left unchanged.
2. **`--category` is a plain string.** On `add`, empty/omitted → `None`. On `modify`, empty string clears the category; omitted leaves it unchanged.
3. **List filters are post-load (in-memory)** matching the existing `--priority` and `--status` filter pattern in `handle_list`. Tag filter: exact tag in `todo.tags`. Category filter: `todo.category == value`.
4. **Column order:** `... Due | Created At | Tags | Category`. `Tags` joined with `", "`, width capped at 30 with `...` truncation. `Category` width capped at 20 with `...` truncation.

## Risks / Trade-offs

- [Repeatable `--tag` UX] → `action="append"` is the standard argparse pattern; documented in help text.
- [Column width] → Capped widths keep the table readable; long tag lists are truncated.
