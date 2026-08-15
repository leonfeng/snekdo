## ADDED Requirements

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

The system SHALL filter all todo list operations by the authenticated user's ID extracted from the JWT token.

#### Scenario: List returns only user's todos

- **WHEN** an authenticated user with token for user A sends `GET /api/v1/todos`
- **THEN** the response contains only todos created by user A

#### Scenario: Create associates todo with user

- **WHEN** an authenticated user with token for user A sends `POST /api/v1/todos`
- **THEN** the created todo is associated with user A

### Requirement: Access token from login is accepted

The system SHALL accept the `access_token` returned by `POST /api/v1/auth/login` as a valid JWT token in the `Authorization` header.

#### Scenario: Login token works for API requests

- **WHEN** a user logs in and receives an `access_token`
- **THEN** subsequent requests with `Authorization: Bearer <access_token>` are authenticated
