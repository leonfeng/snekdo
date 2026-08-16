## Purpose

Defines end-to-end browser tests for showing todo details in the snekdo web
frontend, verifying that users can view the full details of a single todo and
that non-existent todos return a 404 response.

## ADDED Requirements

### Requirement: Show todo details works end-to-end

The system SHALL verify that a user can view the details of a single todo.

#### Scenario: Show todo details page

- **WHEN** a user navigates to `/todos/{id}`
- **THEN** the page displays the todo's title, description, due date, priority,
  status, and created at

#### Scenario: Non-existent todo shows 404

- **WHEN** a user navigates to `/todos/nonexistent-id`
- **THEN** the server returns a 404 response