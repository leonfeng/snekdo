## ADDED Requirements

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

## MODIFIED Requirements

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
