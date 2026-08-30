## Purpose

This capability enables the snekdo CLI to synchronize local todo data with a running FastAPI server via a new `snekdo sync` command, supporting pull, push, and bidirectional sync directions with conflict resolution.

## Requirements

### Requirement: Sync subcommand exists

The system SHALL provide a `snekdo sync` subcommand accessible from the CLI.

#### Scenario: Sync subcommand is recognized

- **WHEN** a user runs `snekdo sync --help`
- **THEN** the system displays help information for the sync command

### Requirement: Server URL configuration

The system SHALL accept a `--server` flag on the `sync` command specifying the server base URL.

#### Scenario: Default server URL

- **WHEN** a user runs `snekdo sync --direction pull` without `--server`
- **THEN** the system connects to `http://127.0.0.1:8000`

#### Scenario: Custom server URL

- **WHEN** a user runs `snekdo sync --direction pull --server http://localhost:9000`
- **THEN** the system connects to `http://localhost:9000`

### Requirement: Pull direction

The system SHALL pull todos from the server into the local storage when `--direction pull` is specified.

#### Scenario: Pull overwrites local storage

- **WHEN** a user runs `snekdo sync --direction pull --storage /tmp/local.json`
- **THEN** the local storage file `/tmp/local.json` is updated to match the server's todo list

#### Scenario: Pull with empty local storage

- **WHEN** the local storage is empty and a user runs `snekdo sync --direction pull`
- **THEN** the local storage is populated with all todos from the server

### Requirement: Push direction

The system SHALL push local todos to the server when `--direction push` is specified.

#### Scenario: Push creates new todos on server

- **WHEN** a user runs `snekdo sync --direction push --storage /tmp/local.json`
- **THEN** todos that exist locally but not on the server are created on the server

#### Scenario: Push updates existing todos on server

- **WHEN** a user runs `snekdo sync --direction push` with local changes to existing todos
- **THEN** the server's todos are updated to match the local state

### Requirement: Both direction

The system SHALL perform both pull and push when `--direction both` is specified.

#### Scenario: Both directions sync

- **WHEN** a user runs `snekdo sync --direction both`
- **THEN** the local storage and server are synchronized in both directions

### Requirement: Conflict resolution

The system SHALL resolve conflicts when a todo exists on both the local storage and the server with diverging state.

#### Scenario: Conflict resolution uses server state

- **WHEN** a todo exists on both local and server with different titles
- **THEN** the server state is used as the source of truth during a `pull` or `both` sync

#### Scenario: Conflict resolution uses local state for push

- **WHEN** a todo exists on both local and server with different titles during a `push`
- **THEN** the local state is used as the source of truth for the push operation

### Requirement: Server unavailable handling

The system SHALL handle a server that is unavailable gracefully.

#### Scenario: Server connection refused

- **WHEN** the server is not running and the user runs `snekdo sync`
- **THEN** the system prints an error message and exits with a non-zero status

#### Scenario: Invalid server URL

- **WHEN** the user provides an invalid URL and runs `snekdo sync`
- **THEN** the system prints an error message and exits with a non-zero status

### Requirement: Storage flag compatibility

The system SHALL accept the `--storage` flag on the `sync` command to specify the local storage path.

#### Scenario: Sync with custom storage

- **WHEN** a user runs `snekdo sync --storage /tmp/custom.json --direction pull`
- **THEN** the system reads from and writes to `/tmp/custom.json`

### Requirement: Sync output

The system SHALL report the sync results to the user.

#### Scenario: Sync summary printed

- **WHEN** a user runs `snekdo sync --direction pull`
- **THEN** the system prints a summary of how many todos were pulled, pushed, or updated

### Requirement: Sync sends authentication token

The system SHALL send the stored access token in the `Authorization: Bearer <token>` header when synchronizing with the server.

#### Scenario: Sync with stored token

- **WHEN** a user has logged in and a token is stored
- **THEN** `snekdo sync` sends the token with each server request

#### Scenario: Sync without token fails gracefully

- **WHEN** a user has not logged in and runs `snekdo sync`
- **THEN** the system reports an authentication error and exits with a non-zero status

### Requirement: Sync handles 401/403 responses

The system SHALL treat HTTP 401 (Unauthorized) and 403 (Forbidden) responses as authentication failures.

#### Scenario: 401 during sync reports error

- **WHEN** the server returns `401` during a sync operation
- **THEN** the system prints an error message indicating authentication is required

#### Scenario: 403 during sync reports error

- **WHEN** the server returns `403` during a sync operation
- **THEN** the system prints an error message indicating access is forbidden

### Requirement: Push sync includes completed status

The system SHALL include the local todo's `completed` field when pushing updates to existing todos on the server.

#### Scenario: Push sync updates completed status

- **WHEN** a local todo is marked complete and the user runs `snekdo sync --direction push`
- **THEN** the server's todo is updated to `completed: true`

#### Scenario: Push sync preserves completed status

- **WHEN** a local todo is incomplete and the user runs `snekdo sync --direction push`
- **THEN** the server's todo is updated to `completed: false`

### Requirement: Both sync includes completed status

The system SHALL include the local todo's `completed` field when `--direction both` is specified.

#### Scenario: Both sync updates completed status

- **WHEN** a local todo is marked complete and the user runs `snekdo sync --direction both`
- **THEN** the server's todo is updated to `completed: true`

### Requirement: Pull sync stores completed status

The system SHALL store the server's `completed` value in the local todo during a pull or both sync.

#### Scenario: Pull sync stores completed status

- **WHEN** the server has a completed todo and the user runs `snekdo sync --direction pull`
- **THEN** the local storage records the todo as `completed: true`

### Requirement: CLI register subcommand

The system SHALL provide a `snekdo register` subcommand that allows a user to create an account from the terminal.

#### Scenario: Register subcommand exists

- **WHEN** a user runs `snekdo register --help`
- **THEN** the system displays help information for the register command

#### Scenario: Register creates account

- **WHEN** a user runs `snekdo register --username <user> --password <pass>`
- **THEN** the system creates the account on the server and stores the access token

### Requirement: CLI login subcommand

The system SHALL provide a `snekdo login` subcommand that authenticates a user and stores the access token.

#### Scenario: Login subcommand exists

- **WHEN** a user runs `snekdo login --help`
- **THEN** the system displays help information for the login command

#### Scenario: Login stores token

- **WHEN** a user runs `snekdo login --username <user> --password <pass>`
- **THEN** the system authenticates and stores the access token for future commands

### Requirement: Sync client sends complete todo payloads

The sync client SHALL include `tags` (list of strings) and `category` (string or null) in the JSON payloads sent for creating and updating todos, so the fields round-trip between local storage and the server.

#### Scenario: Push new todo carries tags and category

- **WHEN** a local todo with `tags=["work"]` and `category="office"` is pushed to the server
- **THEN** the created remote todo has those same `tags` and `category` values

#### Scenario: Push modified todo carries updated tags and category

- **WHEN** a local todo's `tags` or `category` has changed and it is pushed
- **THEN** the remote todo reflects the updated values

#### Scenario: Pull preserves tags and category

- **WHEN** a remote todo has `tags` and `category` and is pulled to local storage
- **THEN** the local todo has those same values

#### Scenario: Todo without tags or category round-trips safely

- **WHEN** a todo with no tags and no category is pushed and pulled
- **THEN** the local copy ends up with `tags == []` and `category is None`
