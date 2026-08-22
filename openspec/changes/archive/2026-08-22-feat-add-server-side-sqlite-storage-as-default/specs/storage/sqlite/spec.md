## ADDED Requirements

### Requirement: SQLite storage backend
The system SHALL use SQLite as the storage backend for todos.

#### Scenario: Successful SQLite connection
- **GIVEN** the application is starting with SQLite storage
- **WHEN** the storage is initialized
- **THEN** a SQLite database file is created at the configured path

#### Scenario: Todo persistence with SQLite
- **GIVEN** a todo item exists
- **WHEN** the todo is saved
- **THEN** the todo is stored in the SQLite database and can be retrieved

#### Scenario: Todo retrieval from SQLite
- **GIVEN** todos are stored in SQLite
- **WHEN** todos are loaded
- **THEN** all todos are returned in the correct order

#### Scenario: Todo modification with SQLite
- **GIVEN** a todo exists in SQLite storage
- **WHEN** the todo is modified
- **THEN** the changes are persisted and reflect on the next load

#### Scenario: Todo deletion with SQLite
- **GIVEN** a todo exists in SQLite storage
- **WHEN** the todo is deleted
- **THEN** the todo is removed and no longer appears on load
