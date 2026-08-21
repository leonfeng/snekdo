## Purpose

Defines end-to-end browser tests for viewing the user profile in the snekdo web
frontend, verifying that logged-in users can view their profile information.

## Requirements

### Requirement: Profile page works end-to-end

The system SHALL verify that a logged-in user can view their profile.

#### Scenario: Profile page renders

- **WHEN** a logged-in user navigates to `/profile`
- **THEN** the page displays the user's username, display name, email, and
  created at
