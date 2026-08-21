## ADDED Requirements

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
