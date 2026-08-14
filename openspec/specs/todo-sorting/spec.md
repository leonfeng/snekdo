# todo-sorting Specification

## Purpose

This capability allows users to control the order of todos when listing them, supporting multiple sort fields and directions to help users organize their workflow effectively.

## Requirements

### Requirement: Sort by created date

The system SHALL allow users to sort todos by their creation date when listing, using proper datetime comparison.

#### Scenario: Sort by newest first (default)

- **WHEN** user runs `list` command without sort flags
- **THEN** system displays todos with newest first (existing behavior)

#### Scenario: Sort by oldest first

- **WHEN** user runs `list --sort created_at --reverse`
- **THEN** system displays todos with oldest first

#### Scenario: Sort by created date descending

- **WHEN** user runs `list --sort created_at --reverse`
- **THEN** system displays todos sorted by creation date in descending order

### Requirement: created_at sorting uses datetime comparison

The system SHALL sort todos by `created_at` using proper datetime comparison, not string comparison.

#### Scenario: Chronological order with microsecond precision

- **WHEN** user runs `list --sort created_at` with todos whose `created_at` values include microseconds (e.g., `2024-01-01T00:00:00.123456` and `2024-01-01T00:00:00.654321`)
- **THEN** system displays todos in correct chronological order

#### Scenario: Reverse chronological order

- **WHEN** user runs `list --sort created_at --reverse` with todos created at different times
- **THEN** system displays todos from newest to oldest using datetime ordering

#### Scenario: Empty created_at values

- **WHEN** user runs `list --sort created_at` with some todos having empty `created_at` values
- **THEN** system places todos with empty `created_at` values consistently (treated as earliest)

#### Scenario: Mixed format created_at values

- **WHEN** user runs `list --sort created_at` with todos whose `created_at` values are in valid ISO 8601 format but with varying precision (e.g., `2024-01-01T00:00:00` and `2024-01-01T00:00:00.000000`)
- **THEN** system sorts them in correct chronological order

### Requirement: Sort by title

The system SHALL allow users to sort todos by their title when listing.

#### Scenario: Sort by title alphabetically

- **WHEN** user runs `list --sort title`
- **THEN** system displays todos sorted by title in ascending alphabetical order

#### Scenario: Sort by title reverse alphabetically

- **WHEN** user runs `list --sort title --reverse`
- **THEN** system displays todos sorted by title in descending alphabetical order

### Requirement: Sort by priority

The system SHALL allow users to sort todos by their priority level when listing.

#### Scenario: Sort by priority (high to low)

- **WHEN** user runs `list --sort priority`
- **THEN** system displays todos with high priority first, then medium, then low

#### Scenario: Sort by priority (low to high)

- **WHEN** user runs `list --sort priority --reverse`
- **THEN** system displays todos with low priority first, then medium, then high

#### Scenario: Sort by priority with equal values

- **WHEN** user runs `list --sort priority` with todos of mixed priorities
- **THEN** system groups todos of the same priority together

### Requirement: Sort by completion status

The system SHALL allow users to sort todos by their completion status when listing.

#### Scenario: Sort by completion status

- **WHEN** user runs `list --sort completed`
- **THEN** system displays incomplete todos first, then completed todos

#### Scenario: Sort by completion status reversed

- **WHEN** user runs `list --sort completed --reverse`
- **THEN** system displays completed todos first, then incomplete todos

### Requirement: Combine sort with filters

The system SHALL apply sorting after filtering by status and priority.

#### Scenario: Sort filtered list

- **WHEN** user runs `list --status pending --sort created_at`
- **THEN** system displays only pending todos sorted by creation date

#### Scenario: Sort with limit

- **WHEN** user runs `list --limit 5 --sort created_at`
- **THEN** system displays the top 5 most recent todos

### Requirement: Handle empty list

The system SHALL handle sorting when the todo list is empty.

#### Scenario: Sort empty list

- **WHEN** user runs `list --sort created_at` with no todos
- **THEN** system displays "No todos found." message

### Requirement: Handle invalid sort field

The system SHALL handle invalid sort field values gracefully.

#### Scenario: Invalid sort field

- **WHEN** user runs `list --sort invalid_field`
- **THEN** system displays an error message and returns non-zero exit code

### Requirement: Handle missing value

The system SHALL handle sorting when some todos have missing values for the sort field.

#### Scenario: Sort by title with empty titles

- **WHEN** user runs `list --sort title` with todos having empty titles
- **THEN** system places empty titles first (or last, consistently)
