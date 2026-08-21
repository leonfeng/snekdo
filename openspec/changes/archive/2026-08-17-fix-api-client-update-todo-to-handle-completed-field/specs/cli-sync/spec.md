## ADDED Requirements

### Requirement: Push sync includes completed status

The system SHALL include the local todo's `completed` field when pushing updates to existing todos on the server.

#### Scenario: Push sync updates completed status

- **WHEN** a local todo is marked complete and the user runs `snekdo sync --direction push`
- **THEN** the server's todo is updated to `completed: true`

#### Scenario: Push sync preserves completed status

- **WHEN** a local todo is incomplete and the user runs `snekdo sync --direction push`
- **THEN** the server's todo is updated to `completed: false`

### Requirement: Both sync includes completed status

The system SHALL include the local todo's `completed` field when `--direction both` is specified.

#### Scenario: Both sync updates completed status

- **WHEN** a local todo is marked complete and the user runs `snekdo sync --direction both`
- **THEN** the server's todo is updated to `completed: true`

### Requirement: Pull sync stores completed status

The system SHALL store the server's `completed` value in the local todo during a pull or both sync.

#### Scenario: Pull sync stores completed status

- **WHEN** the server has a completed todo and the user runs `snekdo sync --direction pull`
- **THEN** the local storage records the todo as `completed: true`