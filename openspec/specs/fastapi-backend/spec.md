## Purpose

This capability exposes the existing snekdo todo storage as a REST API using FastAPI, enabling programmatic access to create, read, update, delete, and list todo items over HTTP.

## Requirements

### Requirement: Health check endpoint

The system SHALL provide a `GET /api/v1/health` endpoint that returns a JSON response indicating the service is healthy.

#### Scenario: Health check returns OK

- **WHEN** a client sends `GET /api/v1/health`
- **THEN** the server responds with status `200` and JSON body `{"status": "ok"}`

### Requirement: OpenAPI schema endpoint

The system SHALL expose an OpenAPI schema at `GET /api/v1/openapi.json`.

#### Scenario: OpenAPI schema is available

- **WHEN** a client sends `GET /api/v1/openapi.json`
- **THEN** the server responds with status `200` and valid JSON describing the OpenAPI schema

### Requirement: List todos via API

The system SHALL provide a `GET /api/v1/todos` endpoint that returns todos as JSON,
defaulting to the `pending` status filter when no `status` query parameter is
specified.

#### Scenario: List todos returns JSON array

- **WHEN** a client sends `GET /api/v1/todos`
- **THEN** the server responds with status `200` and a JSON array of pending todo objects

#### Scenario: Empty list returns empty array

- **WHEN** no todos exist and a client sends `GET /api/v1/todos`
- **THEN** the server responds with status `200` and an empty JSON array `[]`

### Requirement: List todos defaults to pending

The system SHALL default the `status` query parameter of `GET /api/v1/todos` to
`pending`, so that only pending todos are returned when the client does not
explicitly specify a status filter. This matches the CLI `list` command behavior.

#### Scenario: List todos defaults to pending filter

- **WHEN** a client sends `GET /api/v1/todos` without a `status` query parameter
- **THEN** the server responds with status `200` and a JSON array containing only
  pending todos (todos where `completed` is `false`)

#### Scenario: List todos with explicit status=all returns all

- **WHEN** a client sends `GET /api/v1/todos?status=all`
- **THEN** the server responds with status `200` and a JSON array containing all
  todos (pending and completed)

### Requirement: Show todo by ID via API

The system SHALL provide a `GET /api/v1/todos/{todo_id}` endpoint that returns a single todo.

#### Scenario: Show existing todo

- **WHEN** a client sends `GET /api/v1/todos/{valid-id}`
- **THEN** the server responds with status `200` and the todo object as JSON

#### Scenario: Show non-existent todo

- **WHEN** a client sends `GET /api/v1/todos/{non-existent-id}`
- **THEN** the server responds with status `404` and a JSON error message

### Requirement: Add todo via API

The system SHALL provide a `POST /api/v1/todos` endpoint that creates a new todo. The request body MAY include `tags` (a list of strings, default empty list) and `category` (an optional string, default null).

#### Scenario: Add todo successfully

- **WHEN** a client sends `POST /api/v1/todos` with a JSON body containing `title`
- **THEN** the server responds with status `201` and the created todo object

#### Scenario: Add todo missing title

- **WHEN** a client sends `POST /api/v1/todos` with a JSON body missing `title`
- **THEN** the server responds with status `422` and a validation error message

#### Scenario: Add todo with invalid due date

- **WHEN** a client sends `POST /api/v1/todos` with `due: "not-a-date"`
- **THEN** the server responds with status `422` and a validation error message

#### Scenario: Add todo with tags and category

- **WHEN** a client sends `POST /api/v1/todos` with `{"title": "x", "tags": ["work"], "category": "office"}`
- **THEN** the server responds with status `201` and the created todo includes `"tags": ["work"]` and `"category": "office"`

### Requirement: Complete todo via API

The system SHALL provide a `POST /api/v1/todos/{todo_id}/complete` endpoint.

#### Scenario: Complete existing todo

- **WHEN** a client sends `POST /api/v1/todos/{valid-id}/complete`
- **THEN** the server responds with status `200` and the updated todo object

#### Scenario: Complete non-existent todo

- **WHEN** a client sends `POST /api/v1/todos/{non-existent-id}/complete`
- **THEN** the server responds with status `404` and a JSON error message

### Requirement: Modify todo via API

The system SHALL provide a `PUT /api/v1/todos/{todo_id}` endpoint that updates an existing todo. The request body MAY include `tags` (a list of strings that replaces the existing list) and `category` (a string or null).

#### Scenario: Modify todo successfully

- **WHEN** a client sends `PUT /api/v1/todos/{valid-id}` with JSON body containing `title`
- **THEN** the server responds with status `200` and the updated todo object

#### Scenario: Modify non-existent todo

- **WHEN** a client sends `PUT /api/v1/todos/{non-existent-id}`
- **THEN** the server responds with status `404` and a JSON error message

#### Scenario: Modify todo tags

- **WHEN** a client sends `PUT /api/v1/todos/{valid-id}` with `{"tags": ["home", "urgent"]}`
- **THEN** the server responds with status `200` and the todo's tags are replaced with `["home", "urgent"]`

#### Scenario: Modify todo category

- **WHEN** a client sends `PUT /api/v1/todos/{valid-id}` with `{"category": "home"}`
- **THEN** the server responds with status `200` and the todo's category is `"home"`

#### Scenario: Clear todo category via API

- **WHEN** a client sends `PUT /api/v1/todos/{valid-id}` with `{"category": null}`
- **THEN** the server responds with status `200` and the todo's category is cleared (null)

### Requirement: Delete todo via API

The system SHALL provide a `DELETE /api/v1/todos/{todo_id}` endpoint.

#### Scenario: Delete existing todo

- **WHEN** a client sends `DELETE /api/v1/todos/{valid-id}`
- **THEN** the server responds with status `200` and a JSON message confirming deletion

#### Scenario: Delete non-existent todo

- **WHEN** a client sends `DELETE /api/v1/todos/{non-existent-id}`
- **THEN** the server responds with status `404` and a JSON error message

### Requirement: Storage path from CLI is respected

The system SHALL use the storage path provided via the `--storage` flag when the server is started.

#### Scenario: Custom storage path

- **WHEN** the server is started with `snekdo serve --storage /tmp/todos.json`
- **THEN** all API requests read from and write to `/tmp/todos.json`

### Requirement: Server starts and listens

The system SHALL start a FastAPI server with uvicorn when `snekdo serve` is
run, serving both the REST API at `/api/v1/*` and the HTMX/Jinja2 web
frontend at `/` and `/todos/*`.

#### Scenario: Server starts on default port with web UI

- **WHEN** the user runs `snekdo serve`
- **THEN** the server starts and listens on `127.0.0.1:8000` by default,
  serving the web UI at `/` and the API at `/api/v1/*`

#### Scenario: Server starts on custom port with web UI

- **WHEN** the user runs `snekdo serve --host 0.0.0.0 --port 9000`
- **THEN** the server starts and listens on `0.0.0.0:9000`, serving the
  web UI at `/` and the API at `/api/v1/*`

### Requirement: Todo endpoints require authentication

The system SHALL require a valid JWT token (passed via the `Authorization: Bearer <token>` header) for all todo CRUD endpoints (`GET /api/v1/todos`, `GET /api/v1/todos/{id}`, `POST /api/v1/todos`, `PUT /api/v1/todos/{id}`, `DELETE /api/v1/todos/{id}`, `POST /api/v1/todos/{id}/complete`).

#### Scenario: Unauthenticated GET todos returns 401

- **WHEN** a client sends `GET /api/v1/todos` without an `Authorization` header
- **THEN** the server responds with status `401`

#### Scenario: Unauthenticated POST todos returns 401

- **WHEN** a client sends `POST /api/v1/todos` without an `Authorization` header
- **THEN** the server responds with status `401`

#### Scenario: Unauthenticated PUT todos returns 401

- **WHEN** a client sends `PUT /api/v1/todos/{id}` without an `Authorization` header
- **THEN** the server responds with status `401`

#### Scenario: Unauthenticated DELETE todos returns 401

- **WHEN** a client sends `DELETE /api/v1/todos/{id}` without an `Authorization` header
- **THEN** the server responds with status `401`

#### Scenario: Health check does not require authentication

- **WHEN** a client sends `GET /api/v1/health` without an `Authorization` header
- **THEN** the server responds with status `200`

### Requirement: Per-user todo filtering

The system SHALL filter all todo operations — including list, show, create,
complete, modify, and delete — by the authenticated user's ID extracted from
the JWT token. Every mutation endpoint must restrict its storage operation to
the current user's own todos.

#### Scenario: List returns only user's todos

- **WHEN** an authenticated user with token for user A sends `GET /api/v1/todos`
- **THEN** the response contains only todos created by user A

#### Scenario: Create associates todo with user

- **WHEN** an authenticated user with token for user A sends `POST /api/v1/todos`
- **THEN** the created todo is associated with user A

#### Scenario: Complete restricts to user's own todo

- **WHEN** an authenticated user with token for user A sends
  `POST /api/v1/todos/{user-b-todo-id}/complete`
- **THEN** the server responds with status `404` and the todo remains uncompleted

#### Scenario: Modify restricts to user's own todo

- **WHEN** an authenticated user with token for user A sends `PUT`
  `/api/v1/todos/{user-b-todo-id}` with valid update data
- **THEN** the server responds with status `404` and user B's todo is unchanged

#### Scenario: Delete restricts to user's own todo

- **WHEN** an authenticated user with token for user A sends `DELETE`
  `/api/v1/todos/{user-b-todo-id}`
- **THEN** the server responds with status `404` and user B's todo is not deleted

### Requirement: Access token from login is accepted

The system SHALL accept the `access_token` returned by `POST /api/v1/auth/login` as a valid JWT token in the `Authorization` header.

#### Scenario: Login token works for API requests

- **WHEN** a user logs in and receives an `access_token`
- **THEN** subsequent requests with `Authorization: Bearer <access_token>` are authenticated

### Requirement: List todos filtered by tag via API

The system SHALL support an optional `tag` query parameter on `GET /api/v1/todos` that filters results to todos containing that tag.

#### Scenario: Filter by tag

- **WHEN** a client sends `GET /api/v1/todos?tag=work`
- **THEN** the server responds with status `200` and a JSON array of todos whose tags include "work"

#### Scenario: Filter by non-existent tag

- **WHEN** a client sends `GET /api/v1/todos?tag=nonexistent`
- **THEN** the server responds with status `200` and an empty JSON array `[]`

### Requirement: List todos filtered by category via API

The system SHALL support an optional `category` query parameter on `GET /api/v1/todos` that filters results to todos with that exact category.

#### Scenario: Filter by category

- **WHEN** a client sends `GET /api/v1/todos?category=home`
- **THEN** the server responds with status `200` and a JSON array of todos with category "home"

#### Scenario: Filter by non-existent category

- **WHEN** a client sends `GET /api/v1/todos?category=nonexistent`
- **THEN** the server responds with status `200` and an empty JSON array `[]`

### Requirement: TodoResponse includes tags and category

The system SHALL include `tags` and `category` in the `TodoResponse` JSON returned by all todo endpoints.

#### Scenario: Response includes tags and category

- **WHEN** a client sends `GET /api/v1/todos/{valid-id}`
- **THEN** the response JSON includes a `tags` field (array of strings) and a `category` field (string or null)
