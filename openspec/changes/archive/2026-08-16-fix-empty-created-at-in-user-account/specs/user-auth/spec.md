## ADDED Requirements

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
