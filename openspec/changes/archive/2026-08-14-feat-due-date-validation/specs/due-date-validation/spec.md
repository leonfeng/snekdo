## Purpose

This capability defines the validation rules for due dates when adding and modifying todo items. It ensures that due dates are well-formed, in the correct format, and not in the past.

## ADDED Requirements

### Requirement: Validate due date format

The system SHALL validate that the `--due` argument is in valid ISO 8601 date format (YYYY-MM-DD) when provided to the `add` or `modify` command.

#### Scenario: Valid date accepted

- **WHEN** user runs `add --title "Test" --due "2024-12-31"`
- **THEN** system accepts the due date and creates the todo

#### Scenario: Invalid date format rejected

- **WHEN** user runs `add --title "Test" --due "not-a-date"`
- **THEN** system rejects the due date and displays an error message

#### Scenario: Invalid month rejected

- **WHEN** user runs `add --title "Test" --due "2024-13-45"`
- **THEN** system rejects the due date and displays an error message

### Requirement: Validate due date is not in the past

The system SHALL reject due dates that are before the current date.

#### Scenario: Past date rejected

- **WHEN** user runs `add --title "Test" --due "2020-01-01"` (assuming current date is 2024-01-01)
- **THEN** system rejects the due date and displays an error message

#### Scenario: Today's date accepted

- **WHEN** user runs `add --title "Test" --due "2024-01-01"` (assuming current date is 2024-01-01)
- **THEN** system accepts the due date

#### Scenario: Future date accepted

- **WHEN** user runs `add --title "Test" --due "2025-12-31"`
- **THEN** system accepts the due date

### Requirement: Clear error message

The system SHALL display a clear error message when the due date is invalid.

#### Scenario: Error message for invalid format

- **WHEN** user runs `add --title "Test" --due "not-a-date"`
- **THEN** system displays an error message indicating the date format is invalid

#### Scenario: Error message for past date

- **WHEN** user runs `add --title "Test" --due "2020-01-01"`
- **THEN** system displays an error message indicating the date is in the past

### Requirement: Validation applies to modify command

The system SHALL apply the same validation rules to the `modify` command when `--due` is provided.

#### Scenario: Modify with invalid date rejected

- **WHEN** user runs `modify <todo-id> --due "not-a-date"`
- **THEN** system rejects the due date and displays an error message

#### Scenario: Modify with valid date accepted

- **WHEN** user runs `modify <todo-id> --due "2025-12-31"`
- **THEN** system accepts the due date and updates the todo

### Requirement: Empty due date is allowed

The system SHALL allow the `--due` argument to be omitted or empty without error.

#### Scenario: Omitted due date is allowed

- **WHEN** user runs `add --title "Test"` without `--due`
- **THEN** system creates the todo with no due date

#### Scenario: Empty due date is allowed

- **WHEN** user runs `add --title "Test" --due ""`
- **THEN** system creates the todo with no due date

## Existing Behavior

- The `add` command previously accepted any string as the due date
- The `modify` command previously accepted any string as the due date
- No validation was performed on the date format or value
