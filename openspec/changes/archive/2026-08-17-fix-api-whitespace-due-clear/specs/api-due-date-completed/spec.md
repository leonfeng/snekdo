## MODIFIED Requirements

### Requirement: PUT with empty string due preserves existing due date

The system SHALL preserve the existing due date when a client sends `PUT
/api/v1/todos/{id}` with an empty or whitespace-only `due` value.

#### Scenario: PUT with empty string due preserves existing due date

- **WHEN** a client sends `PUT /api/v1/todos/{valid-id}` with `{"due": ""}`
- **THEN** the server responds with status `200` and the updated todo object
- **AND** the stored todo's `due` field is unchanged (empty string is treated as not provided)

#### Scenario: PUT with whitespace-only due preserves existing due date

- **WHEN** a client sends `PUT /api/v1/todos/{valid-id}` with `{"due": "   "}`
- **THEN** the server responds with status `200` and the updated todo object
- **AND** the stored todo's `due` field is unchanged (whitespace-only string is
  treated as not provided, preserving the current value)
