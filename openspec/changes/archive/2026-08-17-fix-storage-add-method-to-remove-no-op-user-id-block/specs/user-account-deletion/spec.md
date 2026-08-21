## MODIFIED Requirements

### Requirement: Storage methods for account deletion

The system SHALL provide `delete_user_with_todos(user_id, todo_storage)` on `UserStorage` and `delete_all_user_todos(user_id)` on `TodoStorage` to support cascading deletion. `delete_user_with_todos` removes both the user record and all todos belonging to that user in a single operation.

#### Scenario: UserStorage.delete_user_with_todos removes user and todos

- **WHEN** `UserStorage.delete_user_with_todos(user_id, todo_storage)` is called with a valid user ID
- **THEN** all todos belonging to that user are removed from the todo storage file
- **AND** the user record is removed from the user storage file
- **AND** todos belonging to other users are preserved

#### Scenario: UserStorage.delete_user removes user

- **WHEN** `UserStorage.delete_user(user_id)` is called with a valid user ID
- **THEN** the user record is removed from the user storage file

#### Scenario: TodoStorage.delete_all_user_todos removes user's todos

- **WHEN** `TodoStorage.delete_all_user_todos(user_id)` is called with a valid user ID
- **THEN** all todos belonging to that user are removed from the todo storage file
- **AND** todos belonging to other users are preserved