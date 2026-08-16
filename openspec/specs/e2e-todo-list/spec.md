## Purpose

Defines end-to-end browser tests for the todo list page of the snekdo web
frontend, verifying that pending todos are displayed correctly and an empty
list shows an appropriate placeholder.

## Requirements

### Requirement: Todo list page works end-to-end

The system SHALL verify that the todo list page displays pending todos and
handles an empty list.

#### Scenario: Empty list shows placeholder

- **WHEN** a logged-in user navigates to `/todos` with no todos
- **THEN** the page displays a "No todos found" message

#### Scenario: List shows todo rows

- **WHEN** a logged-in user navigates to `/todos` with pending todos
- **THEN** the page displays a table with rows for each pending todo
