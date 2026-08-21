## Purpose

Defines end-to-end browser tests for adding a todo in the snekdo web frontend,
verifying that users can create new todos and receive appropriate feedback for
invalid input.

## Requirements

### Requirement: Add todo works end-to-end

The system SHALL verify that a user can add a new todo from the web form.

#### Scenario: Add todo successfully

- **WHEN** a user fills in a title on `/todos/add` and submits
- **THEN** the todo is created and the user is redirected to `/todos`

#### Scenario: Add todo with empty title shows error

- **WHEN** a user submits the add form with an empty title
- **THEN** the form is re-rendered with a "Title is required" error
