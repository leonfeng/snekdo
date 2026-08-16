## Purpose

This capability provides the server-side API for authenticated users to delete their own account, including cascading deletion of all associated todos and token invalidation.

## ADDED Requirements

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
