## 1. Setup dependencies

- [x] 1.1 Add `jinja2` to `dependencies` in `pyproject.toml`.
- [x] 1.2 Create `snekdo/templates/` directory for Jinja2 templates.

## 2. Create the web module

- [x] 2.1 Create `snekdo/web.py` with a FastAPI web app (`WebApp` or similar).
- [x] 2.2 Initialize a Jinja2 `Environment` with `FileSystemLoader` pointing to
  `snekdo/templates/`.
- [x] 2.3 Inject `TodoStorage` via FastAPI `Depends` into all route handlers.
- [x] 2.4 Implement `GET /` and `GET /todos` (list todos, pending by default).
- [x] 2.5 Implement `GET /todos/add` (render add form).
- [x] 2.6 Implement `POST /todos/add` (create todo, redirect to list).
- [x] 2.7 Implement `GET /todos/{id}` (show todo details).
- [x] 2.8 Implement `GET /todos/{id}/edit` (render edit form).
- [x] 2.9 Implement `POST /todos/{id}/edit` (update todo, redirect to list).
- [x] 2.10 Implement `POST /todos/{id}/complete` via HTMX (toggle completion).
- [x] 2.11 Implement `POST /todos/{id}/delete` via HTMX (delete todo, redirect to list).
- [x] 2.12 Add error handling for 404 (not found) and 422 (validation error).

## 3. Create Jinja2 templates

- [x] 3.1 Create `snekdo/templates/base.html` with the page layout, HTMX CDN
  script tag, and basic CSS.
- [x] 3.2 Create `snekdo/templates/list.html` with the todo table matching the
  CLI display conventions.
- [x] 3.3 Create `snekdo/templates/add.html` with the add todo form.
- [x] 3.4 Create `snekdo/templates/edit.html` with the edit todo form.
- [x] 3.5 Create `snekdo/templates/show.html` with the todo detail view.

## 4. Update the `serve` subcommand

- [x] 4.1 Update `handle_serve()` in `snekdo/__main__.py` to mount the web app
  alongside the API app.
- [x] 4.2 Ensure `snekdo serve` serves both `/api/v1/*` and the web UI at `/`.

## 5. Add tests

- [x] 5.1 Create `tests/test_web.py` with tests for the web routes.
- [x] 5.2 Add tests for the list, add, show, edit, complete, and delete pages.
- [x] 5.3 Add tests for HTMX partial-update endpoints.
- [x] 5.4 Add tests for 404 handling.

## 6. Update documentation

- [x] 6.1 Update `README.md` to describe the web frontend and how to access it.
- [x] 6.2 Update `README.md` to mention the `jinja2` dependency.
