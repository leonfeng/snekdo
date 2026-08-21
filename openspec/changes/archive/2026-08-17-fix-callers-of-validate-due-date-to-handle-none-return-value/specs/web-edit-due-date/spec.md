## Purpose

The web edit-todo form must preserve an existing due date when the user submits the form without changing it, rather than clearing it.

## ADDED Requirements

### Requirement: Edit todo preserves existing due date when not changed

The system SHALL preserve the existing due date when the user submits the edit form without modifying the due field.

#### Scenario: Edit todo without changing due date preserves it

- **WHEN** a todo has an existing due date of `2024-12-31`
- **AND** a user navigates to `/todos/{id}/edit` and submits the form with the due field left empty
- **THEN** the server updates the todo and redirects to the list page
- **AND** the stored todo still has `due = "2024-12-31"`

#### Scenario: Edit todo with new due date updates it

- **WHEN** a todo has an existing due date of `2024-12-31`
- **AND** a user submits the edit form with a new due date of `2025-06-15`
- **THEN** the server updates the todo and redirects to the list page
- **AND** the stored todo has `due = "2025-06-15"`

#### Scenario: Edit todo with empty due date preserves existing due date

- **WHEN** a todo has an existing due date of `2024-12-31`
- **AND** a user leaves the due field empty in the form
- **THEN** the server updates the todo and redirects to the list page
- **AND** the stored todo still has `due = "2024-12-31"`

### Requirement: Web edit form validates due date format

The system SHALL validate the due date format when the user provides one in the edit form.

#### Scenario: Invalid due date format shows error

- **WHEN** a user submits the edit form with `due = "not-a-date"`
- **THEN** the server renders the edit form with an error message

#### Scenario: Past due date shows error

- **WHEN** a user submits the edit form with a past due date like `2020-01-01`
- **THEN** the server renders the edit form with an error message
