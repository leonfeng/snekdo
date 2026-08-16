## Purpose

This delta adds CLI-level server URL requirements to the existing `user-profile` capability, ensuring the `profile`, `profile-update`, and `change-password` CLI commands accept a `--server` flag.

## ADDED Requirements

### Requirement: CLI profile command accepts server URL

The system SHALL provide a `snekdo profile` subcommand that accepts a `--server` flag specifying the server base URL.

#### Scenario: Profile command uses default server

- **WHEN** a user runs `snekdo profile` without `--server`
- **THEN** the system connects to `http://127.0.0.1:8000`

#### Scenario: Profile command uses custom server

- **WHEN** a user runs `snekdo profile --server http://localhost:9000`
- **THEN** the system connects to `http://localhost:9000`

### Requirement: CLI profile-update command accepts server URL

The system SHALL provide a `snekdo profile-update` subcommand that accepts a `--server` flag specifying the server base URL.

#### Scenario: Profile update uses default server

- **WHEN** a user runs `snekdo profile-update --display-name "New Name"` without `--server`
- **THEN** the system connects to `http://127.0.0.1:8000`

#### Scenario: Profile update uses custom server

- **WHEN** a user runs `snekdo profile-update --display-name "New Name" --server http://localhost:9000`
- **THEN** the system connects to `http://localhost:9000`

### Requirement: CLI change-password command accepts server URL

The system SHALL provide a `snekdo change-password` subcommand that accepts a `--server` flag specifying the server base URL.

#### Scenario: Change password uses default server

- **WHEN** a user runs `snekdo change-password --current-password old --new-password new --confirm-password new` without `--server`
- **THEN** the system connects to `http://127.0.0.1:8000`

#### Scenario: Change password uses custom server

- **WHEN** a user runs `snekdo change-password --current-password old --new-password new --confirm-password new --server http://localhost:9000`
- **THEN** the system connects to `http://localhost:9000`