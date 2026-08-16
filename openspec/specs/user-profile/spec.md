## Purpose

This capability provides authenticated users with the ability to view and manage their own account profile, including displaying their username, display name, email, and account creation timestamp, updating their display name and email, and changing their password.

## Requirements

### Requirement: View own profile

The system SHALL provide a `GET /api/v1/users/me` endpoint that returns the authenticated user's profile information.

#### Scenario: Profile returned successfully

- **WHEN** an authenticated user sends `GET /api/v1/users/me` with a valid `Authorization: Bearer <token>` header
- **THEN** the server responds with status `200` and a JSON response containing the user's `id`, `username`, `display_name`, `email`, and `created_at`

#### Scenario: Unauthenticated access denied

- **WHEN** a client sends `GET /api/v1/users/me` without an `Authorization` header
- **THEN** the server responds with status `401`

### Requirement: Update profile

The system SHALL provide a `PUT /api/v1/users/me` endpoint that allows the authenticated user to update their display name and/or email.

#### Scenario: Update display name succeeds

- **WHEN** an authenticated user sends `PUT /api/v1/users/me` with a JSON body containing `display_name`
- **THEN** the server responds with status `200` and the updated user profile including the new `display_name`

#### Scenario: Update email succeeds

- **WHEN** an authenticated user sends `PUT /api/v1/users/me` with a JSON body containing `email`
- **THEN** the server responds with status `200` and the updated user profile including the new `email`

#### Scenario: Update both fields succeeds

- **WHEN** an authenticated user sends `PUT /api/v1/users/me` with a JSON body containing both `display_name` and `email`
- **THEN** the server responds with status `200` and the updated user profile including both new values

#### Scenario: Update with invalid email format

- **WHEN** an authenticated user sends `PUT /api/v1/users/me` with a JSON body containing an invalid `email` format
- **THEN** the server responds with status `422` and a validation error message

#### Scenario: Unauthenticated access denied

- **WHEN** a client sends `PUT /api/v1/users/me` without an `Authorization` header
- **THEN** the server responds with status `401`

#### Scenario: Empty string clears field

- **WHEN** an authenticated user sends `PUT /api/v1/users/me` with `display_name` set to an empty string `""`
- **THEN** the server responds with status `200` and the user profile has `display_name` set to `null` or empty

### Requirement: Change password

The system SHALL provide a `PUT /api/v1/users/me/password` endpoint that allows the authenticated user to change their password.

#### Scenario: Password change succeeds

- **WHEN** an authenticated user sends `PUT /api/v1/users/me/password` with a JSON body containing `current_password`, `new_password`, and `confirm_password` that match
- **THEN** the server responds with status `200` and a message confirming the password was changed

#### Scenario: Current password is wrong

- **WHEN** an authenticated user sends `PUT /api/v1/users/me/password` with an incorrect `current_password`
- **THEN** the server responds with status `401` or `422` and an authentication error message

#### Scenario: New password too short

- **WHEN** an authenticated user sends `PUT /api/v1/users/me/password` with a `new_password` shorter than 8 characters
- **THEN** the server responds with status `422` and a validation error message

#### Scenario: New password does not match confirmation

- **WHEN** an authenticated user sends `PUT /api/v1/users/me/password` with `new_password` and `confirm_password` that do not match
- **THEN** the server responds with status `422` and a validation error message

#### Scenario: Unauthenticated access denied

- **WHEN** a client sends `PUT /api/v1/users/me/password` without an `Authorization` header
- **THEN** the server responds with status `401`

### Requirement: Profile isolation

The system SHALL ensure that a user can only access and modify their own profile.

#### Scenario: User cannot access another user's profile

- **WHEN** an authenticated user sends `GET /api/v1/users/me` using a token for a different user
- **THEN** the server responds with status `404`

#### Scenario: User cannot modify another user's profile

- **WHEN** an authenticated user sends `PUT /api/v1/users/me` using a token for a different user
- **THEN** the server responds with status `404`

### Requirement: created_at is set at registration

The system SHALL record a non-empty `created_at` timestamp (ISO 8601 format) when registering a new user account.

#### Scenario: created_at is present in profile

- **WHEN** a registered user sends `GET /api/v1/users/me`
- **THEN** the response contains a `created_at` field with a non-empty ISO 8601 timestamp

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
