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

The system SHALL provide a `GET /api/v1/todos` endpoint that returns all todos as JSON.

#### Scenario: List todos returns JSON array

- **WHEN** a client sends `GET /api/v1/todos`
- **THEN** the server responds with status `200` and a JSON array of todo objects

#### Scenario: Empty list returns empty array

- **WHEN** no todos exist and a client sends `GET /api/v1/todos`
- **THEN** the server responds with status `200` and an empty JSON array `[]`

### Requirement: Show todo by ID via API

The system SHALL provide a `GET /api/v1/todos/{todo_id}` endpoint that returns a single todo.

#### Scenario: Show existing todo

- **WHEN** a client sends `GET /api/v1/todos/{valid-id}`
- **THEN** the server responds with status `200` and the todo object as JSON

#### Scenario: Show non-existent todo

- **WHEN** a client sends `GET /api/v1/todos/{non-existent-id}`
- **THEN** the server responds with status `404` and a JSON error message

### Requirement: Add todo via API

The system SHALL provide a `POST /api/v1/todos` endpoint that creates a new todo.

#### Scenario: Add todo successfully

- **WHEN** a client sends `POST /api/v1/todos` with a JSON body containing `title`
- **THEN** the server responds with status `201` and the created todo object

#### Scenario: Add todo missing title

- **WHEN** a client sends `POST /api/v1/todos` with a JSON body missing `title`
- **THEN** the server responds with status `422` and a validation error message

#### Scenario: Add todo with invalid due date

- **WHEN** a client sends `POST /api/v1/todos` with `due: "not-a-date"`
- **THEN** the server responds with status `422` and a validation error message

### Requirement: Complete todo via API

The system SHALL provide a `POST /api/v1/todos/{todo_id}/complete` endpoint.

#### Scenario: Complete existing todo

- **WHEN** a client sends `POST /api/v1/todos/{valid-id}/complete`
- **THEN** the server responds with status `200` and the updated todo object

#### Scenario: Complete non-existent todo

- **WHEN** a client sends `POST /api/v1/todos/{non-existent-id}/complete`
- **THEN** the server responds with status `404` and a JSON error message

### Requirement: Modify todo via API

The system SHALL provide a `PUT /api/v1/todos/{todo_id}` endpoint that updates an existing todo.

#### Scenario: Modify todo successfully

- **WHEN** a client sends `PUT /api/v1/todos/{valid-id}` with JSON body containing `title`
- **THEN** the server responds with status `200` and the updated todo object

#### Scenario: Modify non-existent todo

- **WHEN** a client sends `PUT /api/v1/todos/{non-existent-id}`
- **THEN** the server responds with status `404` and a JSON error message

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

The system SHALL start a FastAPI server with uvicorn when `snekdo serve` is run.

#### Scenario: Server starts on default port

- **WHEN** the user runs `snekdo serve`
- **THEN** the server starts and listens on `127.0.0.1:8000` by default

#### Scenario: Server starts on custom port

- **WHEN** the user runs `snekdo serve --host 0.0.0.0 --port 9000`
- **THEN** the server starts and listens on `0.0.0.0:9000`
