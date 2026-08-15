## Why

snekdo currently only exposes a CLI and a REST API. Users want a browser-based
interface to manage their todos interactively, with partial-page updates that
avoid full form postbacks. Adding an HTMX + Jinja2 frontend delivers that
experience while reusing the existing `TodoStorage` layer and FastAPI server.

## What Changes

- Add a new web frontend capability that renders HTML pages with Jinja2 and
  uses HTMX for interactive, partial-page updates (e.g. complete/delete without
  full reloads).
- Provide CRUD web pages: list todos, add a todo, edit a todo, show a todo,
  complete a todo, and delete a todo.
- Extend the existing `serve` subcommand so it serves both the REST API
  (`/api/v1/*`) and the web UI (`/` and `/todos/*`) on the same host/port.
- Add Jinja2 as a project dependency.
- Add a `web` module (`snekdo/web.py`) that hosts the FastAPI app with Jinja2
  template rendering and HTMX-aware endpoints.

## Capabilities

### New Capabilities

- `htmx-jinja2-frontend`: A web-based todo management interface using Jinja2
  templates and HTMX for interactivity.

### Modified Capabilities

- `fastapi-backend`: The `serve` command and FastAPI app will additionally serve
  static HTML pages and template-rendered views alongside the REST API.

## Impact

- **Code**: New `snekdo/web.py` module, `snekdo/templates/` directory with
  Jinja2 templates, and updates to `snekdo/__main__.py` (serve subcommand).
- **API**: Existing `/api/v1/*` endpoints are unchanged. New web routes are
  added at `/` and `/todos/*`.
- **Dependencies**: `jinja2` added to `dependencies` in `pyproject.toml`.
- **Compatibility**: Fully backward-compatible; the CLI and API continue to
  work exactly as before. The web frontend is an additional access path.
