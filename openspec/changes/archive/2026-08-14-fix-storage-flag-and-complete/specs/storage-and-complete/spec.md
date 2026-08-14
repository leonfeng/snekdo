## Purpose

This change fixes two critical bugs in the CLI layer:
1. The `--storage` flag is parsed but never used, so todos are always saved to the default path.
2. The `complete` command overwrites the entire storage file with only the completed todo, losing all other todos.

## Requirements

### Requirement: Storage path flag must be respected

The system SHALL use the path specified by the `--storage` flag when reading and writing the todos JSON file.

#### Scenario: Custom storage path

- **WHEN** user runs any command with `--storage /path/to/todos.json`
- **THEN** the system reads from and writes to `/path/to/todos.json`

#### Scenario: Default storage path

- **WHEN** user runs any command without `--storage`
- **THEN** the system reads from and writes to `~/.snekdo/todos.json`

#### Scenario: Storage path is used for all commands

- **WHEN** user runs `add`, `list`, `complete`, `delete`, or `modify` with `--storage`
- **THEN** all commands use the specified storage path

### Requirement: Complete must not lose other todos

The system SHALL preserve all todos when marking one as complete.

#### Scenario: Complete one todo preserves others

- **WHEN** user runs `complete <todo-id>` with multiple todos in storage
- **THEN** only the specified todo is marked complete and all other todos remain unchanged

#### Scenario: Complete non-existent todo

- **WHEN** user runs `complete` with an invalid todo ID
- **THEN** the system displays an error message and returns a non-zero exit code

## Implementation Notes

- Use `TodoStorage(storage_path=args.storage)` in every command handler.
- Use `storage.complete(args.todo_id)` instead of manually setting `completed` and saving a single-item list.
