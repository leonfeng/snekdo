## Purpose

This capability defines the expected behavior of the `--debug` flag, ensuring it is accepted on the CLI and produces debug output to stderr when set.

## Requirements

### Requirement: Debug flag is accepted

The system SHALL accept the `--debug` flag before the subcommand (global position) for all commands.

**Note**: argparse does not support boolean flags (`action="store_true"`) in both global and per-subcommand positions simultaneously when defined on both the parent and subparsers. The flag is therefore defined on the parent parser only, making it available before the subcommand.

#### Scenario: Debug flag is accepted globally

- **WHEN** user runs `snekdo --debug list`
- **THEN** the system accepts the flag without error

### Requirement: Debug output is emitted to stderr

The system SHALL print debug information to stderr when `--debug` is set.

#### Scenario: Debug output includes command name

- **WHEN** user runs any command with `--debug`
- **THEN** the system prints a debug message indicating the command being executed (e.g., `DEBUG: command=list`)

#### Scenario: Debug output includes storage path

- **WHEN** user runs any command with `--debug`
- **THEN** the system prints a debug message indicating the effective storage path (e.g., `DEBUG: storage_path=/path/to/todos.json`)

#### Scenario: Debug output is on stderr

- **WHEN** user runs any command with `--debug`
- **THEN** the debug messages are written to stderr, not stdout

### Requirement: Debug output does not affect normal output

The system SHALL ensure that debug output does not interfere with normal command output.

#### Scenario: Normal output unchanged without debug

- **WHEN** user runs a command without `--debug`
- **THEN** the system behaves exactly as before, with no debug messages

#### Scenario: Debug output is separate from command output

- **WHEN** user runs `snekdo --debug list` with todos
- **THEN** debug messages appear on stderr and the todo list appears on stdout

### Requirement: Debug output is suppressed by default

The system SHALL not print debug output when `--debug` is not provided.

#### Scenario: No debug output without flag

- **WHEN** user runs `snekdo list` without `--debug`
- **THEN** no debug messages are printed