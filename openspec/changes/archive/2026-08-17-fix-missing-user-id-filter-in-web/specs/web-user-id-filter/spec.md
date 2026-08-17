## Purpose

Ensures the web frontend consistently filters and persists the `user_id` association for all todos, so todos created via the CLI or API are visible in the web UI for the same user, and the web UI never shows todos belonging to other users.

## ADDED Requirements

### Requirement: Todo serialization includes user_id

The system SHALL serialize the `user_id` field for every `Todo` instance, including when it is `None`, so that the stored JSON faithfully records the user association.

#### Scenario: to_dict includes user_id for owned todo

- **WHEN** a `Todo` with a non-empty `user_id` is serialized via `to_dict()`
- **THEN** the resulting dict contains a `user_id` key equal to the todo's `user_id`

#### Scenario: to_dict includes user_id for unowned todo

- **WHEN** a `Todo` with `user_id` set to `None` is serialized via `to_dict()`
- **THEN** the resulting dict contains a `user_id` key with value `None`

### Requirement: Web list filters by authenticated user_id

The system SHALL filter the todo list in the web UI to only show todos whose `user_id` matches the authenticated user's ID.

#### Scenario: List shows only current user's todos

- **WHEN** an authenticated user navigates to `/todos`
- **THEN** the page displays only todos whose `user_id` equals the authenticated user's ID

#### Scenario: List excludes other users' todos

- **WHEN** an authenticated user navigates to `/todos`
- **THEN** the page does not display todos belonging to other users

#### Scenario: Empty list for user with no todos

- **WHEN** an authenticated user with no todos navigates to `/todos`
- **THEN** the page displays a "No todos found" message

### Requirement: Web add sets user_id

The system SHALL set the `user_id` field on todos created through the web add form to the authenticated user's ID.

#### Scenario: Created todo has user_id

- **WHEN** an authenticated user creates a todo via the web form
- **THEN** the created todo has `user_id` set to the authenticated user's ID

#### Scenario: Created todo is visible in list

- **WHEN** an authenticated user creates a todo via the web form and navigates to the list
- **THEN** the newly created todo appears in the list

### Requirement: CLI add sets user_id

The system SHALL set the `user_id` field on todos created through the CLI to the authenticated user's ID when a user is logged in.

#### Scenario: CLI created todo has user_id

- **WHEN** a logged-in user creates a todo via the CLI
- **THEN** the created todo has `user_id` set to the logged-in user's ID

#### Scenario: CLI created todo visible in web

- **WHEN** a logged-in user creates a todo via the CLI and then views the web UI
- **THEN** the CLI-created todo is visible in the web list

## MODIFIED Requirements

### Requirement: Web UI is served alongside the API

**MODIFIED**: The web UI now consistently filters todos by the authenticated user's `user_id` for all list endpoints, ensuring per-user isolation in the web interface.

#### Scenario: Web list is filtered by user_id

- **WHEN** an authenticated user navigates to `/todos` or `/`
- **THEN** the server renders an HTML table listing only pending todos whose `user_id` matches the authenticated user's ID

### Requirement: Per-user todo isolation

**MODIFIED**: The web frontend now enforces per-user isolation by filtering todos by `user_id` at the storage layer, in addition to the API.

#### Scenario: Web user sees only their own todos

- **WHEN** an authenticated user sends `GET /todos` via the web UI
- **THEN** the response contains only todos belonging to that user

#### Scenario: Web user cannot access another user's todo

- **WHEN** an authenticated user navigates to `/todos/{other-user-todo-id}`
- **THEN** the server returns a 404 response

## REMOVED Requirements

### Requirement: None

**Reason**: No requirements are removed in this change.