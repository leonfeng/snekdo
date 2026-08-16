## Purpose

This capability provides authenticated users with a way to delete their own account and all associated data, covering the API, storage, HTTP client, CLI, and web frontend.

## Requirements

### Requirement: Delete account endpoint

The system SHALL provide a `DELETE /api/v1/users/me` endpoint that allows an authenticated user to delete their own account.

#### Scenario: Account deletion succeeds with password confirmation

- **WHEN** an authenticated user sends `DELETE /api/v1/users/me` with a JSON body containing a valid `password`
- **THEN** the server responds with status `200` and a JSON message confirming the account was deleted
- **AND** the user record is removed from the user storage
- **AND** all todos belonging to the user are removed from the todo storage

#### Scenario: Account deletion with wrong password fails

- **WHEN** an authenticated user sends `DELETE /api/v1/users/me` with an incorrect `password`
- **THEN** the server responds with status `401` and an authentication error message

#### Scenario: Unauthenticated access denied

- **WHEN** a client sends `DELETE /api/v1/users/me` without an `Authorization` header
- **THEN** the server responds with status `401`

#### Scenario: Invalid token denied

- **WHEN** a client sends `DELETE /api/v1/users/me` with an invalid `Authorization` token
- **THEN** the server responds with status `401`

#### Scenario: Password field is required

- **WHEN** an authenticated user sends `DELETE /api/v1/users/me` with an empty or missing `password` field
- **THEN** the server responds with status `422` and a validation error message

### Requirement: Cascading deletion of user todos

The system SHALL delete all todos belonging to the deleted user when the account is deleted.

#### Scenario: All user todos are deleted

- **WHEN** an authenticated user deletes their account
- **THEN** all todos with `user_id` equal to the deleted user's ID are removed from the todo storage

#### Scenario: Other users' todos are preserved

- **WHEN** an authenticated user deletes their own account
- **THEN** todos belonging to other users remain in the todo storage

### Requirement: Token invalidation after deletion

The system SHALL ensure that a deleted user's JWT token cannot be used to authenticate.

#### Scenario: Deleted user token is rejected

- **WHEN** a client sends a request with a JWT token for a deleted user
- **THEN** the server responds with status `401`

### Requirement: Storage methods for account deletion

The system SHALL provide `delete_user(user_id)` on `UserStorage` and `delete_all_user_todos(user_id)` on `TodoStorage` to support cascading deletion.

#### Scenario: UserStorage.delete_user removes user

- **WHEN** `UserStorage.delete_user(user_id)` is called with a valid user ID
- **THEN** the user record is removed from the user storage file

#### Scenario: TodoStorage.delete_all_user_todos removes user's todos

- **WHEN** `TodoStorage.delete_all_user_todos(user_id)` is called with a valid user ID
- **THEN** all todos belonging to that user are removed from the todo storage file
- **AND** todos belonging to other users are preserved

### Requirement: API client delete_account method

The system SHALL provide a `delete_account(password, credentials_path)` method on `ServerHttpClient` that deletes the current user's account.

#### Scenario: Client delete account succeeds

- **WHEN** `ServerHttpClient.delete_account(password=...)` is called with a valid password
- **THEN** the method returns the message response dict
- **AND** the account is deleted on the server

#### Scenario: Client delete account with wrong password fails

- **WHEN** `ServerHttpClient.delete_account(password=...)` is called with an incorrect password
- **THEN** the method raises `AuthenticationError`

#### Scenario: Client delete account without credentials fails

- **WHEN** `ServerHttpClient.delete_account()` is called without stored credentials
- **THEN** the method raises `AuthenticationError`

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

### Requirement: Delete account option on profile page

The system SHALL provide a delete account option on the authenticated user's profile page.

#### Scenario: Delete account button is shown

- **WHEN** an authenticated user navigates to `/profile`
- **THEN** the page includes a "Delete account" button or link

#### Scenario: Unauthenticated access redirects to login

- **WHEN** an unauthenticated user navigates to `/profile`
- **THEN** the server redirects to `/auth/login`

### Requirement: Delete account confirmation

The system SHALL require confirmation before deleting the account.

#### Scenario: Delete account confirmation dialog

- **WHEN** a user clicks the "Delete account" button
- **THEN** the user is prompted to confirm the deletion (e.g., JavaScript `confirm()` dialog)

#### Scenario: Delete account password confirmation

- **WHEN** a user confirms the deletion
- **THEN** the user is prompted to enter their password

#### Scenario: Delete account succeeds

- **WHEN** a user confirms deletion and enters the correct password
- **THEN** the account is deleted
- **AND** the user is redirected to `/auth/login`

#### Scenario: Delete account with wrong password fails

- **WHEN** a user confirms deletion but enters an incorrect password
- **THEN** the account is not deleted
- **AND** an error message is shown
