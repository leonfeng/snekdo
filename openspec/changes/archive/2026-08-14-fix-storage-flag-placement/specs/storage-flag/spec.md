## Purpose

This capability defines the expected behavior of the `--storage` flag, ensuring it is accepted in both global (before subcommand) and per-subcommand (after subcommand) positions across all CLI commands.

## ADDED Requirements

### Requirement: Storage flag accepted globally

The system SHALL accept the `--storage` flag as a global option before the subcommand for all commands.

#### Scenario: Storage flag before subcommand

- **WHEN** user runs `snekdo --storage /path/to/todos.json list`
- **THEN** the system reads todos from `/path/to/todos.json`

#### Scenario: Storage flag before subcommand for add

- **WHEN** user runs `snekdo --storage /path/to/todos.json add --title "Test"`
- **THEN** the system saves the new todo to `/path/to/todos.json`

### Requirement: Storage flag accepted per-subcommand

The system SHALL accept the `--storage` flag after the subcommand for all commands.

#### Scenario: Storage flag after subcommand

- **WHEN** user runs `snekdo list --storage /path/to/todos.json`
- **THEN** the system reads todos from `/path/to/todos.json`

#### Scenario: Storage flag after subcommand for add

- **WHEN** user runs `snekdo add --storage /path/to/todos.json --title "Test"`
- **THEN** the system saves the new todo to `/path/to/todos.json`

### Requirement: Storage flag applies to all commands

The system SHALL accept the `--storage` flag for every subcommand: add, list, complete, delete, modify, and show.

#### Scenario: Storage flag with complete

- **WHEN** user runs `snekdo complete --storage /path/to/todos.json <todo-id>`
- **THEN** the system marks the todo as complete in `/path/to/todos.json`

#### Scenario: Storage flag with delete

- **WHEN** user runs `snekdo delete --storage /path/to/todos.json <todo-id>`
- **THEN** the system deletes the todo from `/path/to/todos.json`

#### Scenario: Storage flag with modify

- **WHEN** user runs `snekdo modify --storage /path/to/todos.json <todo-id> --title "New Title"`
- **THEN** the system updates the todo in `/path/to/todos.json`

#### Scenario: Storage flag with show

- **WHEN** user runs `snekdo show --storage /path/to/todos.json <todo-id>`
- **THEN** the system displays the todo from `/path/to/todos.json`

### Requirement: Storage flag default behavior

The system SHALL use the default storage path (`~/.snekdo/todos.json`) when `--storage` is not provided.

#### Scenario: Default storage path

- **WHEN** user runs `snekdo list` without `--storage`
- **THEN** the system reads todos from `~/.snekdo/todos.json`
