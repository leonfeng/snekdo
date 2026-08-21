## Purpose

Defines end-to-end browser tests for the user login flow of the snekdo web
frontend, verifying that existing users can authenticate and receive
appropriate feedback for invalid credentials.

## Requirements

### Requirement: Login flow works end-to-end

The system SHALL verify that an existing user can log in and is redirected to
the todo list.

#### Scenario: Login with valid credentials

- **WHEN** a user enters a valid username and password on `/auth/login` and
  submits
- **THEN** the user is authenticated and redirected to `/todos`

#### Scenario: Login with invalid credentials

- **WHEN** a user enters an invalid username or password
- **THEN** the login form is re-rendered with an error message
