## MODIFIED Requirements

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

#### Scenario: PUT without due field does not clear existing due date

- **WHEN** a client sends `PUT /api/v1/todos/{valid-id}` with `{"title": "new title"}`
- **THEN** the server responds with status `200` and the updated todo object
- **AND** the stored todo's `due` field is unchanged

#### Scenario: PUT with empty string due preserves existing due date

- **WHEN** a client sends `PUT /api/v1/todos/{valid-id}` with `{"due": ""}`
- **THEN** the server responds with status `200` and the updated todo object
- **AND** the stored todo's `due` field is unchanged (empty string is treated as not provided)
