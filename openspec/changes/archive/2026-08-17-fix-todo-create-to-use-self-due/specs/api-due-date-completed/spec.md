## ADDED Requirements

### Requirement: TodoCreate.to_todo validates the due date

The `TodoCreate.to_todo()` method SHALL validate the `due` field so that the
produced `Todo` object never stores an invalid due-date string.  Invalid or
empty due values MUST be normalized to `None`.

#### Scenario: Valid future due date preserved

- **WHEN** `TodoCreate(title="Test", due="2027-12-31").to_todo()` is called
- **THEN** the resulting `Todo` has `due == "2027-12-31"`

#### Scenario: Empty string due date becomes None

- **WHEN** `TodoCreate(title="Test", due="").to_todo()` is called
- **THEN** the resulting `Todo` has `due is None`

#### Scenario: None due date stays None

- **WHEN** `TodoCreate(title="Test").to_todo()` is called (default due=None)
- **THEN** the resulting `Todo` has `due is None`

#### Scenario: Invalid due date raises ValueError

- **WHEN** `TodoCreate(title="Test", due="not-a-date").to_todo()` is called
- **THEN** a `ValueError` is raised

#### Scenario: Past due date raises ValueError

- **WHEN** `TodoCreate(title="Test", due="2020-01-01").to_todo()` is called
- **THEN** a `ValueError` is raised
