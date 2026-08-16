## Purpose

This capability defines the general server URL configuration for all CLI commands that connect to a FastAPI server. Every server-facing CLI command MUST accept a `--server` flag and default to `http://127.0.0.1:8000`.

## Requirements

### Requirement: Server URL flag on all server-facing CLI commands

The system SHALL accept a `--server` flag on every CLI subcommand that connects to the FastAPI server, with a default value of `http://127.0.0.1:8000`.

#### Scenario: Default server URL for profile command

- **WHEN** a user runs `snekdo profile` without `--server`
- **THEN** the system connects to `http://127.0.0.1:8000`

#### Scenario: Custom server URL for profile command

- **WHEN** a user runs `snekdo profile --server http://localhost:9000`
- **THEN** the system connects to `http://localhost:9000`

#### Scenario: Default server URL for profile-update command

- **WHEN** a user runs `snekdo profile-update --display-name "New Name"` without `--server`
- **THEN** the system connects to `http://127.0.0.1:8000`

#### Scenario: Custom server URL for profile-update command

- **WHEN** a user runs `snekdo profile-update --display-name "New Name" --server http://localhost:9000`
- **THEN** the system connects to `http://localhost:9000`

#### Scenario: Default server URL for change-password command

- **WHEN** a user runs `snekdo change-password --current-password old --new-password new --confirm-password new` without `--server`
- **THEN** the system connects to `http://127.0.0.1:8000`

#### Scenario: Custom server URL for change-password command

- **WHEN** a user runs `snekdo change-password --current-password old --new-password new --confirm-password new --server http://localhost:9000`
- **THEN** the system connects to `http://localhost:9000`

#### Scenario: Default server URL for delete-account command

- **WHEN** a user runs `snekdo delete-account --password pass` without `--server`
- **THEN** the system connects to `http://127.0.0.1:8000`

#### Scenario: Custom server URL for delete-account command

- **WHEN** a user runs `snekdo delete-account --password pass --server http://localhost:9000`
- **THEN** the system connects to `http://localhost:9000`

### Requirement: Server URL passed to HTTP client

The system SHALL pass the resolved `--server` value to `ServerHttpClient` as `base_url` for every server-facing CLI command.

#### Scenario: Profile command uses custom server

- **WHEN** a user runs `snekdo profile --server http://localhost:9000`
- **THEN** `ServerHttpClient` is initialized with `base_url="http://localhost:9000"`

#### Scenario: Delete-account command uses custom server

- **WHEN** a user runs `snekdo delete-account --password pass --server http://localhost:9000`
- **THEN** `ServerHttpClient` is initialized with `base_url="http://localhost:9000"`