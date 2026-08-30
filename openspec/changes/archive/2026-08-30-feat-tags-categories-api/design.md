## Context

See proposal for motivation. `snekdo/api.py` defines Pydantic models `TodoCreate`, `TodoUpdate`, `TodoResponse` and handlers in `create_app()`. The `Todo` model and storage already support `tags`/`category` (model + storage slices).

## Goals / Non-Goals

**Goals:**
- Accept `tags` and `category` in `TodoCreate`/`TodoUpdate`.
- Return them in `TodoResponse`.
- Support `tag` and `category` query filters on `GET /api/v1/todos`.

**Non-Goals:**
- No changes to CLI, storage, or web templates.

## Decisions

1. **`TodoCreate.tags` defaults to `[]`; `TodoCreate.category` defaults to `None`.** Matches the model defaults.
2. **`TodoUpdate.tags` is `Optional[list[str]]` and `TodoUpdate.category` is `Optional[str]`.** `None` means "not provided" (leave unchanged); an explicit `tags=[]` clears the list; an explicit `category=None` in JSON clears the category.
3. **List endpoint filters in-memory** after loading, consistent with existing status/priority filtering. Tag filter: exact tag present in `todo.tags`. Category filter: `todo.category == value`.

## Risks / Trade-offs

- [Ambiguity of `category=None` in PUT] → `TodoUpdate.category` uses `Optional[str]` with `None` sentinel meaning "not provided". To clear the category, the client sends `category: null` explicitly, which is distinguished from the field being absent by checking the raw dict or using a sentinel. Simpler approach: treat `category` in the update payload as "set to this value, None clears" — since Pydantic cannot distinguish absent from explicit null without extra machinery, the spec says `category=null` clears it. This is acceptable for the current API surface.
- [In-memory filter performance] → Acceptable at personal-list scale.
