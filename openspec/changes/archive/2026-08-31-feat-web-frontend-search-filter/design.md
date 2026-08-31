## Context

The web frontend in `snekdo/web.py` serves Jinja2 templates at `/todos` and `/` with HTMX for partial updates. Currently, the list endpoint (`list_todos` at line 121) loads all todos via `storage.load(user_id=user_id)` and filters only by `completed` status in Python, then renders the full `list.html` template. The template at `snekdo/templates/list.html` has no filter controls — it renders a single table with a collapsed `<details>` section for completed todos.

The REST API (`snekdo/api.py:330-384`) already supports `status`, `priority`, and `tag` query params on `GET /api/v1/todos`, but no `q` (text search) param.

## Goals / Non-Goals

**Goals:**
- Add `q`, `status`, and `priority` query parameters to the web list routes
- Extract shared filter logic into a reusable helper function
- Add a filter bar (search input + status select + priority select) to the list template
- Wire HTMX for partial table updates on filter changes (debounced search, instant dropdown changes)
- Make the completed-todos `<details>` section conditional (only shown when `status != pending` and completed todos exist in the filtered set)

**Non-Goals:**
- No changes to the REST API endpoints
- No changes to storage layer or models
- No new database indexes or full-text search
- No changes to the CLI
- No sort/order controls on the web frontend (that's a separate concern)

## Decisions

### 1. Filter logic as a shared helper function

**Decision:** Add a `_filter_todos(todos, q=None, status="pending", priority=None)` function in `web.py` that encapsulates all filter logic. Both `index` and `list_todos` routes call it.

**Rationale:** The two routes (`/` and `/todos`) currently duplicate the pending-filter logic. Extracting to a helper eliminates duplication and makes it easy to add more filters later. The REST API has its own filtering inline in `list_todos` — we do NOT refactor that to use the same helper, since the API has additional concerns (sort, limit, different param names).

**Alternative considered:** Refactoring `api.py`'s `list_todos` to share the helper. Rejected because the API's filter logic is more complex (includes sort + limit) and changing it risks breaking existing API behavior.

### 2. Case-insensitive substring search via `str.lower()`

**Decision:** Use Python's `in` operator on lowercased strings for title and description matching.

**Rationale:** The dataset is small (hundreds to low thousands of todos per user). A Python-level `in` check is sufficient and requires no dependencies. SQLAlchemy's `ilike`/`lower()` would only matter if we pushed filtering into the storage layer, which we're not doing.

**Alternative considered:** Using `storage.load()` with a new `search` param. Rejected — would require changing the storage interface and both JSON and SQLite backends.

### 3. `status` param replaces the hardcoded pending filter

**Decision:** The `status` query param accepts `"pending"` (default), `"completed"`, or `"all"`. This replaces the current hardcoded `pending = [t for t in todos if not t.completed]` logic.

**Rationale:** Makes the existing default behavior (show pending only) explicit and overridable. The `<details>` collapse for completed todos becomes redundant when `status=all` is selected, so it's shown conditionally.

### 4. HTMX wiring for the filter bar

**Decision:** The search input uses `hx-get` with `hx-trigger="keyup changed delay:300ms"` and the two `<select>` elements use `hx-get` with `hx-trigger="change"`. All target `#todo-table-wrapper` (a new wrapper div around the table) with `hx-swap="outerHTML"`. The server returns the full list template (which re-renders the filter bar with current values) but HTMX only swaps the wrapper element.

**Rationale:** Using a wrapper div around the table (not the whole page) means the filter bar itself is replaced on each response, keeping the input values in sync with the URL. The 300ms debounce on the search input avoids excessive requests while typing.

**Alternative considered:** Using `hx-target` on just the `<tbody>`. Rejected because the empty-state `<p>` and the `<details>` section are siblings of the table, so we need a wrapper to swap all of them atomically.

### 5. Template context passes current filter values

**Decision:** The template receives `q`, `status`, and `priority` in the context so the filter bar inputs can be pre-filled with the current selections.

**Rationale:** Without this, after an HTMX swap, the filter bar would reset to defaults.

## Risks / Trade-offs

- **Performance on large lists:** Filtering happens in Python after loading all todos from storage. For a single user's todos (typically <1000), this is negligible. If this becomes a bottleneck, the filter logic could be pushed into `storage.load()` as query params.
- **HTMX swap of full list template:** The server renders the entire `list.html` template (including the filter bar) for each filter change. This is slightly wasteful vs. rendering only the table fragment, but it's simpler and the templates are small.
- **Debounce timing:** 300ms may feel sluggish on fast typing. This is a tunable constant in the template.
