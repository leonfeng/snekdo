## ADDED Requirements

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
