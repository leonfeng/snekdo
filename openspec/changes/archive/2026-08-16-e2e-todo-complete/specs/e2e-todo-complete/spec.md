## Purpose

Defines end-to-end browser tests for completing a todo in the snekdo web
frontend, verifying that users can mark todos as complete via both HTMX and
traditional redirect.

## ADDED Requirements

### Requirement: Complete todo works end-to-end

The system SHALL verify that a user can mark a todo as complete via HTMX.

#### Scenario: Complete todo via HTMX updates row

- **WHEN** a user clicks the complete button on a todo row
- **THEN** the row updates to show the completed status without a full page
  reload

#### Scenario: Complete todo via redirect

- **WHEN** a user clicks the complete button without HTMX
- **THEN** the user is redirected to `/todos`