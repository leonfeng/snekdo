## Purpose

This capability provides the CLI command for authenticated users to delete their own account on the server.

## ADDED Requirements

### Requirement: CLI delete-account command

The system SHALL provide a `snekdo delete-account` subcommand that deletes the current user's account on the server.

#### Scenario: CLI delete account succeeds

- **WHEN** a user runs `snekdo delete-account --password <password>` with valid credentials stored locally
- **THEN** the account is deleted on the server
- **AND** the stored credentials are removed from disk
- **AND** a success message is printed

#### Scenario: CLI delete account with wrong password fails

- **WHEN** a user runs `snekdo delete-account --password <wrong-password>` with valid credentials stored locally
- **THEN** the account is not deleted
- **AND** an error message is printed

#### Scenario: CLI delete account without server connection fails

- **WHEN** a user runs `snekdo delete-account` when the server is not reachable
- **THEN** a connection error is printed

#### Scenario: CLI delete account without stored credentials fails

- **WHEN** a user runs `snekdo delete-account` without stored credentials
- **THEN** an authentication error is printed
