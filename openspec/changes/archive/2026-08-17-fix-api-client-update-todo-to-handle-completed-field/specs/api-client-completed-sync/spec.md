## Purpose

This capability ensures that the API client's `update_todo` method and the CLI sync function properly handle the `completed` field when synchronizing todos, so the completion status is consistent between the local storage and the server.

## ADDED Requirements

### Requirement: API client update_todo accepts completed

The `ServerHttpClient.update_todo()` method SHALL accept a `completed` parameter and include it in the request body when provided.

#### Scenario: update_todo includes completed in request

- **WHEN** a client calls `update_todo(todo_id="...", completed=True)`
- **THEN** the server receives `{"completed": true}` in the request body

#### Scenario: update_todo includes completed false

- **WHEN** a client calls `update_todo(todo_id="...", completed=False)`
- **THEN** the server receives `{"completed": false}` in the request body

#### Scenario: update_todo omits completed when not provided

- **WHEN** a client calls `update_todo(todo_id="...")` without `completed`
- **THEN** the request body does not contain a `completed` key

### Requirement: Sync passes completed during push

The `snekdo sync --direction push` command SHALL pass the local todo's `completed` value when updating an existing todo on the server.

#### Scenario: Push sync updates completed status

- **WHEN** a local todo is marked complete and the user runs `snekdo sync --direction push`
- **THEN** the server's todo is updated to `completed: true`

#### Scenario: Push sync preserves completed status

- **WHEN** a local todo is incomplete and the user runs `snekdo sync --direction push`
- **THEN** the server's todo is updated to `completed: false`

### Requirement: Sync passes completed during both

The `snekdo sync --direction both` command SHALL pass the local todo's `completed` value when updating an existing todo on the server.

#### Scenario: Both sync updates completed status

- **WHEN** a local todo is marked complete and the user runs `snekdo sync --direction both`
- **THEN** the server's todo is updated to `completed: true`

### Requirement: Sync receives completed from server on pull

The `snekdo sync --direction pull` command SHALL store the server's `completed` value in the local todo.

#### Scenario: Pull sync stores completed status

- **WHEN** the server has a completed todo and the user runs `snekdo sync --direction pull`
- **THEN** the local storage records the todo as `completed: true`

### Requirement: Sync reports completed changes

The sync command SHALL report the number of todos updated during sync, including completion status changes.

#### Scenario: Sync summary includes completed updates

- **WHEN** a user runs `snekdo sync --direction push` with completed changes
- **THEN** the system prints a summary that includes the number of updated todos

## Test Requirements

- Unit tests MUST verify that `update_todo` includes `completed` in the request body.
- Integration tests MUST verify that `snekdo sync --direction push` updates the server's `completed` status.
- Integration tests MUST verify that `snekdo sync --direction pull` stores the server's `completed` status.