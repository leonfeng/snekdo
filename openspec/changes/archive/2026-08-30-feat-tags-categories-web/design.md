## Context

See proposal for motivation. The web layer is Jinja2 + HTMX in `snekdo/web.py` with templates in `snekdo/templates/`. The add/edit forms are standard HTML forms that POST to the web handlers; the list view renders rows via `list_row.html` partial.

## Goals / Non-Goals

**Goals:**
- Add a comma-separated `tags` input and a `category` input to the add and edit forms.
- Parse comma-separated tags in the web handlers (split on comma, trim, drop empties, dedupe preserving order).
- Display `Tags` and `Category` columns in the list view.

**Non-Goals:**
- No tag-input widget (comma-separated text is sufficient).
- No drag-drop or kanban.

## Decisions

1. **Comma-separated text input for tags.** Simplest approach that works with standard HTML forms and HTMX. The handler splits on comma, strips whitespace, drops empty tokens, and dedupes while preserving order.
2. **Category is a plain text input.** Single string, empty → `None`.
3. **List columns follow existing dynamic-width pattern.** `Tags` capped at 30, `Category` capped at 20, single-space separators.

## Risks / Trade-offs

- [Comma-separated parsing] → Trim and filter empties to handle trailing commas and extra spaces.
