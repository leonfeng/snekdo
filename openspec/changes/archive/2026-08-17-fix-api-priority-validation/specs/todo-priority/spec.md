## ADDED Requirements

### Requirement: Validate priority values via API

The system SHALL validate that priority values provided through the FastAPI REST
API (`POST /api/v1/todos` and `PUT /api/v1/todos/{id}`) are one of: `low`,
`medium`, `high`.

#### Scenario: Invalid priority value via API returns 422

- **WHEN** a client sends `POST /api/v1/todos` with `{"title": "x", "priority": "urgent"}`
- **THEN** the server responds with status `422` and a validation error message

#### Scenario: Invalid priority value via PUT returns 422

- **WHEN** a client sends `PUT /api/v1/todos/{valid-id}` with `{"priority": "critical"}`
- **THEN** the server responds with status `422` and a validation error message

#### Scenario: Valid priority value via API is accepted

- **WHEN** a client sends `POST /api/v1/todos` with `{"title": "x", "priority": "high"}`
- **THEN** the server responds with status `201` and the created todo object with
  `"priority": "high"`
