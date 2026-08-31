## Why

The web todo list (`/todos` and `/`) shows every pending todo for the
authenticated user with no way to search or filter. As the list grows, users
must scroll through all rows to find a specific todo. The CLI already supports
filtering by status and priority; the web frontend should offer equivalent
search and filter controls.

## What Changes

- Add a search box to the web todo list page that filters todos by a
  case-insensitive substring match on title and description.
- Add a status filter (all / pending / completed) to the web list page.
- Add a priority filter (all / high / medium / low) to the web list page.
- Filters combine (AND semantics) and are driven by `q`, `status`, and
  `priority` query parameters on the list routes.
- The existing completed-todos `<details>` collapse is removed; completed
  todos are shown inline in the table (filtered out when `status=pending`),
  and the count in the summary reflects the current filter.
- The filter bar (search + status + priority) re-renders into a named
  container via HTMX when any control changes, without a full page reload.

## Capabilities

### New Capabilities

- `web-search-filter`: Search and filter controls (by title/description
  text, status, and priority) on the web todo list page, combining
  server-side filtering with HTMX partial updates.

### Modified Capabilities

- `htmx-jinja2-frontend`: The "List todos via web UI" requirement changes —
  the list page now renders a filter bar and reflects the `status` and
  `priority` query parameters instead of always showing all pending todos.

## Impact

- `snekdo/web.py`: list routes gain `q`/`status`/`priority` query params and
  a shared filtering helper.
- `snekdo/templates/list.html`: filter bar markup and HTMX wiring; drop the
  completed-todos `<details>` collapse.
- `tests/`: web route tests for the new filter parameters and an e2e test
  exercising the filter bar.
- No REST API or storage changes; CLI behavior is unaffected.
