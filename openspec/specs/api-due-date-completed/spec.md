## Purpose

This capability exposes the existing snekdo todo storage as a REST API using FastAPI, enabling programmatic access to create, read, update, delete, and list todo items over HTTP.

## Requirements

### Requirement: API stores due date as null when not provided

The system SHALL store `due` as `null` (Python `None`) in the JSON storage when a todo is created or updated without a due date.

#### Scenario: Create todo without due date stores null

- **WHEN** a client sends `POST /api/v1/todos` with `title` only (no `due`)
- **THEN** the stored todo has `due: null` in the JSON file
- **AND** the API response includes `"due": null`

#### Scenario: Update todo without due date stores null

- **WHEN** a client sends `PUT /api/v1/todos/{id}` with `title` only (no `due`)
- **THEN** the stored todo's `due` remains `null`
- **AND** the API response includes `"due": null`

### Requirement: API supports updating completed status via PUT

The system SHALL accept `completed` as a field in the `PUT /api/v1/todos/{id}` request body and update the todo's completion status.

#### Scenario: Update completed status via PUT

- **WHEN** a client sends `PUT /api/v1/todos/{valid-id}` with `{"completed": true}`
- **THEN** the server responds with status `200` and the updated todo object with `"completed": true`
- **AND** the stored todo has `completed: true`

#### Scenario: Update completed status to false via PUT

- **WHEN** a client sends `PUT /api/v1/todos/{valid-id}` with `{"completed": false}`
- **THEN** the server responds with status `200` and the updated todo object with `"completed": false`

#### Scenario: PUT without completed field does not error

- **WHEN** a client sends `PUT /api/v1/todos/{valid-id}` with `{"title": "new title"}`
- **THEN** the server responds with status `200` and the updated todo object
- **AND** the todo's `completed` field is unchanged

### Requirement: API validate_due_date returns null for empty dates

The system SHALL return `null` (Python `None`) from the internal `_validate_due_date` helper when given an empty or `None` input.

#### Scenario: Empty due date returns null

- **WHEN** `_validate_due_date("")` is called
- **THEN** the result is `None`

#### Scenario: None due date returns null

- **WHEN** `_validate_due_date(None)` is called
- **THEN** the result is `None`