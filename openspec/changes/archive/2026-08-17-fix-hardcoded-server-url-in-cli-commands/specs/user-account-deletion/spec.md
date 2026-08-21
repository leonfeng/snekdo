## Purpose

This delta adds CLI-level server URL requirements to the existing `user-account-deletion` capability, ensuring the `delete-account` CLI command accepts a `--server` flag.

## ADDED Requirements

### Requirement: CLI delete-account command accepts server URL

The system SHALL provide a `snekdo delete-account` subcommand that accepts a `--server` flag specifying the server base URL.

#### Scenario: Delete account uses default server

- **WHEN** a user runs `snekdo delete-account --password <password>` without `--server`
- **THEN** the system connects to `http://127.0.0.1:8000`

#### Scenario: Delete account uses custom server

- **WHEN** a user runs `snekdo delete-account --password <password> --server http://localhost:9000`
- **THEN** the system connects to `http://localhost:9000`