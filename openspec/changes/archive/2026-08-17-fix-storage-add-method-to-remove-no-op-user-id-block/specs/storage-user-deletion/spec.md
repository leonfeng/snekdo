## Purpose

This capability provides a single storage operation to delete a user account and all associated todo data, ensuring that user deletion is atomic and does not leave orphaned todos.

## ADDED Requirements

### Requirement: UserStorage.delete_user_with_todos removes user and todos

The system SHALL provide a `delete_user_with_todos(user_id, todo_storage)` method on `UserStorage` that removes all todos belonging to the user and then removes the user record.

#### Scenario: User and all their todos are deleted

- **WHEN** `UserStorage.delete_user_with_todos(user_id, todo_storage)` is called with a valid user ID
- **THEN** all todos with `user_id` equal to the given user ID are removed from the todo storage
- **AND** the user record is removed from the user storage

#### Scenario: Other users' todos are preserved

- **WHEN** `UserStorage.delete_user_with_todos(user_id, todo_storage)` is called with a valid user ID
- **THEN** todos belonging to other users remain in the todo storage

#### Scenario: Non-existent user returns False

- **WHEN** `UserStorage.delete_user_with_todos(user_id, todo_storage)` is called with a non-existent user ID
- **THEN** the method returns False
- **AND** no todos are deleted

### Requirement: TodoStorage.delete_all_user_todos preserves other users

The system SHALL preserve todos belonging to other users when deleting one user's todos.

#### Scenario: Other users' todos are preserved

- **WHEN** `TodoStorage.delete_all_user_todos(user_id)` is called
- **THEN** todos belonging to other users remain in the storage

### Requirement: API delete account cascades to todos

The system SHALL delete all todos belonging to the deleted user when the account is deleted.

#### Scenario: All user todos are deleted

- **WHEN** an authenticated user deletes their account
- **THEN** all todos with `user_id` equal to the deleted user's ID are removed from the todo storage

#### Scenario: Other users' todos are preserved

- **WHEN** an authenticated user deletes their own account
- **THEN** todos belonging to other users remain in the todo storage