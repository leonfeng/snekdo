## Purpose

Defines end-to-end browser tests for the user logout flow of the snekdo web
frontend, verifying that logged-in users can invalidate their session and are
redirected to the login page.

## Requirements

### Requirement: Logout works end-to-end

The system SHALL verify that a logged-in user can log out and is redirected to
the login page.

#### Scenario: Logout redirects to login

- **WHEN** a logged-in user clicks the logout link
- **THEN** the session is invalidated and the user is redirected to `/auth/login`
