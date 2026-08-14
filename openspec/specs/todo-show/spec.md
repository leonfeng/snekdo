# todo-show Specification

## Purpose

This capability allows users to view the complete details of a single todo item by its ID, displaying all stored fields in a readable format.

## Requirements

### Requirement: Show todo details command

The system SHALL provide a `show` command that accepts a todo ID and displays all details of the corresponding todo item.

#### Scenario: Show existing todo

- **WHEN** user runs `show <todo-id>` with a valid todo ID
- **THEN** system displays all fields: ID, Title, Description, Due, Priority, Status, and Created At
- **THEN** the output clearly labels each field

#### Scenario: Show non-existent todo

- **WHEN** user runs `show <todo-id>` with an ID that does not exist
- **THEN** system displays an error message indicating the todo was not found
- **THEN** system returns a non-zero exit code

### Requirement: Show displays completed status

The system SHALL display whether a todo is completed or pending.

#### Scenario: Completed status shown

- **WHEN** user runs `show` on a completed todo
- **THEN** system displays "Status: ✓" or "Status: completed"

#### Scenario: Pending status shown

- **WHEN** user runs `show` on a pending todo
- **THEN** system displays "Status: " or "Status: pending"

### Requirement: Show displays created_at

The system SHALL display the `created_at` field when showing todo details.

#### Scenario: Created At displayed

- **WHEN** user runs `show` on a todo
- **THEN** system displays the `created_at` value in ISO 8601 format

#### Scenario: Created At empty

- **WHEN** user runs `show` on a todo with an empty `created_at`
- **THEN** system displays an empty or placeholder value for Created At
