## Context

snekdo already has a CLI (`snekdo/__main__.py`) and a FastAPI REST API
(`snekdo/api.py`) backed by `snekdo/storage.py` and `snekdo/models.py`.
The `serve` subcommand starts uvicorn with the FastAPI app. We need to add a
web frontend that reuses these existing components.

## Goals / Non-Goals

**Goals:**
- Add a Jinja2-rendered web frontend with HTMX for interactive, partial-page
  updates.
- Provide web pages for all CRUD operations on todos.
- Serve the web frontend and the REST API on the same FastAPI server.
- Keep the existing CLI and API behavior unchanged.

**Non-Goals:**
- No authentication or multi-user support.
- No database migration (still uses the JSON file).
- No separate web server process (reuses uvicorn).
- No npm/build step for HTMX (loaded via CDN).

## Decisions

### Decision 1: Use FastAPI + Jinja2 (not a separate framework)

Rationale: The project already depends on FastAPI and uvicorn. Adding Jinja2
(`jinja2` package) lets us render HTML templates within the same FastAPI app,
avoiding a separate web server process. Alternatives considered: Flask,
Starlette with Jinja2, or a separate Node.js frontend. FastAPI + Jinja2 is the
simplest path that reuses existing infrastructure.

### Decision 2: HTMX loaded via CDN

Rationale: The project avoids build tools and npm. Loading HTMX from a CDN
(`https://unpkg.com/htmx.org@2.0.0/dist/htmx.min.js`) in the base template
keeps the frontend dependency-free at build time. Alternatives: bundle HTMX
via npm/pip, but that adds complexity.

### Decision 3: Extend `serve` to serve both API and web UI

Rationale: Users expect `snekdo serve` to just work. Serving both the API and
web UI on the same host/port means a single process serves the CLI sync target
and the browser UI. The API stays at `/api/v1/*`; web routes are at `/` and
`/todos/*`.

### Decision 4: Reuse `TodoStorage` directly in web routes

Rationale: `TodoStorage` is the shared abstraction used by CLI and API.
Injecting it into web routes via FastAPI's `Depends` keeps the data layer
consistent and avoids duplication.

### Decision 5: HTMX `hx-post`/`hx-put`/`hx-delete` for form submissions

Rationale: HTMX allows form submissions via `hx-post`, `hx-put`, `hx-delete`
attributes, which send XHR requests with the form data. The server responds
with the partial HTML to replace the target element. This provides the
"interactive, partial-page update" experience without JavaScript.

### Decision 6: Templates stored in `snekdo/templates/`

Rationale: Jinja2's `TemplateLoader` can load from a directory. Storing
templates in `snekdo/templates/` keeps them bundled with the package so
`pip install` makes them available. The `Jinja2Env` is initialized with
`loader=FileSystemLoader(str(Path(__file__).parent / "templates"))`.

## Risks / Trade-offs

[Risk] HTMX CDN may be unavailable offline.
→ Mitigation: Document that an internet connection is needed for the CDN, or
  allow local HTMX as an alternative.

[Risk] Jinja2 template syntax errors cause 500 errors.
→ Mitigation: Use `DEBUG` mode in development; add error handling in the
  FastAPI app to render a friendly error page.

[Risk] Serving HTML and API from the same app may create coupling.
→ Mitigation: Keep web routes in `snekdo/web.py` and API routes in
  `snekdo/api.py`; both share `TodoStorage` via dependency injection.

## Migration Plan

1. Add `jinja2` to `dependencies` in `pyproject.toml`.
2. Create `snekdo/web.py` with the FastAPI web app and route handlers.
3. Create `snekdo/templates/` with base, list, add, edit, show templates.
4. Update `snekdo/__main__.py` `handle_serve()` to mount the web app alongside
   the API app (or create a combined app).
5. Add tests for the web routes.
6. Update README.md to describe the web frontend.

## Open Questions

- Should the web UI use the existing `/api/v1/*` endpoints via HTMX, or should
  it have its own template-rendered routes? → We use template-rendered routes
  (server-side rendering with Jinja2) for the main pages, with HTMX for
  partial updates that call the same routes.
- What should the default route structure be? → `/` (list), `/todos/add`,
  `/todos/{id}`, `/todos/{id}/edit`, with HTMX forms posting to the relevant
  endpoints.
