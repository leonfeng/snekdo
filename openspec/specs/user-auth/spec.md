## Purpose

This capability provides user registration, login, and JWT-based authentication for the snekdo API, CLI, and web frontend, enabling per-user todo isolation.

## Requirements

### Requirement: User registration endpoint

The system SHALL provide a `POST /api/v1/auth/register` endpoint that creates a new user account from a username and password.

#### Scenario: Registration succeeds

- **WHEN** a client sends `POST /api/v1/auth/register` with a JSON body containing `username` and `password`
- **THEN** the server responds with status `201` and a JSON response containing the user's `id` and `username`

#### Scenario: Registration with missing username

- **WHEN** a client sends `POST /api/v1/auth/register` with a JSON body missing `username`
- **THEN** the server responds with status `422` and a validation error message

#### Scenario: Registration with missing password

- **WHEN** a client sends `POST /api/v1/auth/register` with a JSON body missing `password`
- **THEN** the server responds with status `422` and a validation error message

#### Scenario: Registration with duplicate username

- **WHEN** a client sends `POST /api/v1/auth/register` with a `username` that already exists
- **THEN** the server responds with status `409` and a message indicating the username is already taken

#### Scenario: Password length requirement

- **WHEN** a client sends `POST /api/v1/auth/register` with a `password` shorter than 8 characters
- **THEN** the server responds with status `422` and a validation error message

### Requirement: User login endpoint

The system SHALL provide a `POST /api/v1/auth/login` endpoint that authenticates a user and returns an access token.

#### Scenario: Login succeeds

- **WHEN** a client sends `POST /api/v1/auth/login` with a JSON body containing a valid `username` and `password`
- **THEN** the server responds with status `200` and a JSON response containing an `access_token` and `token_type`

#### Scenario: Login with wrong password

- **WHEN** a client sends `POST /api/v1/auth/login` with an incorrect `password`
- **THEN** the server responds with status `401` and an authentication error message

#### Scenario: Login with unknown username

- **WHEN** a client sends `POST /api/v1/auth/login` with a `username` that does not exist
- **THEN** the server responds with status `401` and an authentication error message

### Requirement: JWT token format

The system SHALL issue JSON Web Tokens (JWT) that contain at minimum the user's `sub` (user ID) and an expiration claim.

#### Scenario: Token contains user ID

- **WHEN** a user logs in successfully
- **THEN** the returned token contains a `sub` claim equal to the user's ID

#### Scenario: Token has expiration

- **WHEN** a user logs in successfully
- **THEN** the returned token contains an `exp` claim that is set to a future time

### Requirement: Authentication required for todo operations

The system SHALL require a valid JWT token for all todo CRUD endpoints.

#### Scenario: Unauthenticated access denied

- **WHEN** a client sends `GET /api/v1/todos` without an `Authorization` header
- **THEN** the server responds with status `401`

#### Scenario: Invalid token denied

- **WHEN** a client sends `GET /api/v1/todos` with an invalid `Authorization` token
- **THEN** the server responds with status `401`

#### Scenario: Expired token denied

- **WHEN** a client sends `GET /api/v1/todos` with an expired token
- **THEN** the server responds with status `401`

### Requirement: Per-user todo isolation

The system SHALL ensure that every user can only access their own todos.

#### Scenario: User sees only their own todos

- **WHEN** an authenticated user sends `GET /api/v1/todos`
- **THEN** the response contains only todos belonging to that user

#### Scenario: User cannot access another user's todo

- **WHEN** an authenticated user sends `GET /api/v1/todos/{other-user-todo-id}`
- **THEN** the server responds with status `404`

#### Scenario: User cannot modify another user's todo

- **WHEN** an authenticated user sends `PUT /api/v1/todos/{other-user-todo-id}`
- **THEN** the server responds with status `404`

#### Scenario: User cannot delete another user's todo

- **WHEN** an authenticated user sends `DELETE /api/v1/todos/{other-user-todo-id}`
- **THEN** the server responds with status `404`

### Requirement: Password storage security

The system SHALL store user passwords as salted hashes and never store plaintext passwords.

#### Scenario: Plaintext password is never stored

- **WHEN** a user registers
- **THEN** the stored user record contains only a hash, not the plaintext password

#### Scenario: Hashing algorithm is used

- **WHEN** a user registers or logs in
- **THEN** the system uses a recognized password hashing library (e.g., passlib/bcrypt)

### Requirement: Authentication endpoint for CLI

The system SHALL provide a way for the CLI to obtain an access token for use with the sync command.

#### Scenario: CLI login obtains token

- **WHEN** a user runs `snekdo login` with valid credentials
- **THEN** the system stores the access token for subsequent commands

### Requirement: Authentication endpoint for web frontend

The system SHALL provide web pages for registration and login via the Jinja2 frontend.

#### Scenario: Registration page is accessible

- **WHEN** a user navigates to `/auth/register`
- **THEN** the system renders a registration form

#### Scenario: Login page is accessible

- **WHEN** a user navigates to `/auth/login`
- **THEN** the system renders a login form

#### Scenario: Login with invalid input re-renders form

- **WHEN** a user submits the login form with an empty username or password
- **THEN** the login form is re-rendered with an HTML error message

#### Scenario: Registration with invalid input re-renders form

- **WHEN** a user submits the registration form with an invalid username or password
- **THEN** the registration form is re-rendered with an HTML error message

### Requirement: Logout

The system SHALL provide a logout endpoint that invalidates the user session. The logout endpoint MUST use the HTTP POST method so that it is not cacheable or CSRF-able.

#### Scenario: Logout redirects to login

- **WHEN** a logged-in user clicks the logout link
- **THEN** the session is invalidated and the user is redirected to `/auth/login`

#### Scenario: Logout requires POST

- **WHEN** a user sends a GET request to the logout endpoint
- **THEN** the server returns a 405 Method Not Allowed response

#### Scenario: Logout invalidates CSRF token

- **WHEN** a user logs out
- **THEN** the CSRF token is also invalidated

### Requirement: User registration records created_at timestamp

The system SHALL record a non-empty `created_at` timestamp (ISO 8601 format) when registering a new user account through any registration interface (API or web).

#### Scenario: API registration sets created_at

- **WHEN** a client sends `POST /api/v1/auth/register` with a valid `username` and `password`
- **THEN** the response contains a `created_at` field with a non-empty ISO 8601 timestamp

#### Scenario: Web registration sets created_at

- **WHEN** a user submits the registration form at `/auth/register` with a valid `username` and `password`
- **THEN** the stored user record contains a non-empty `created_at` field in ISO 8601 format

#### Scenario: created_at is set at registration time

- **WHEN** a new user is registered through any interface
- **THEN** the `created_at` field is set to the current timestamp at the time of registration
