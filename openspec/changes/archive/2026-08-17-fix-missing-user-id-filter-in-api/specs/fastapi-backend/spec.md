## MODIFIED Requirements

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
