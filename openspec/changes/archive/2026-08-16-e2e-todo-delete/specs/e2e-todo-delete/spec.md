## Purpose

Defines end-to-end browser tests for deleting a todo in the snekdo web frontend,
verifying that users can remove todos via both HTMX and traditional redirect.

## ADDED Requirements

### Requirement: Delete todo works end-to-end

The system SHALL verify that a user can delete a todo.

#### Scenario: Delete todo via HTMX removes row

- **WHEN** a user clicks the delete button on a todo row
- **THEN** the row is removed from the table without a full page reload

#### Scenario: Delete todo via redirect

- **WHEN** a user clicks the delete button without HTMX
- **THEN** the user is redirected to `/todos`