## Purpose

Defines end-to-end browser tests for editing a todo in the snekdo web frontend,
verifying that users can update existing todos and receive appropriate feedback
for invalid input.

## Requirements

### Requirement: Edit todo works end-to-end

The system SHALL verify that a user can edit an existing todo.

#### Scenario: Edit form pre-fills values

- **WHEN** a user navigates to `/todos/{id}/edit`
- **THEN** the form is pre-filled with the todo's current title, description,
  due date, and priority

#### Scenario: Edit todo successfully

- **WHEN** a user submits the edit form with updated values
- **THEN** the todo is updated and the user is redirected to `/todos`

#### Scenario: Edit todo with empty title shows error

- **WHEN** a user submits the edit form with an empty title
- **THEN** the form is re-rendered with a "Title is required" error
