## MODIFIED Requirements

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

## ADDED Requirements

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
