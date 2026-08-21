## Purpose

Defines end-to-end browser tests for the user registration flow of the snekdo
web frontend, verifying that new users can create an account and receive
appropriate feedback for invalid input.

## ADDED Requirements

### Requirement: Registration flow works end-to-end

The system SHALL verify that a new user can register and is redirected to the
login page.

#### Scenario: Registration form is submitted

- **WHEN** a user fills in a username and password on `/auth/register` and
  submits the form
- **THEN** the account is created and the user is redirected to `/auth/login`

#### Scenario: Registration with missing fields shows error

- **WHEN** a user submits the registration form with an empty username
- **THEN** the registration form is re-rendered with an error message

### Requirement: Registration with invalid data shows error

The system SHALL verify that registration with invalid input shows an error.

#### Scenario: Registration with short username shows error

- **WHEN** a user submits the registration form with a username shorter than 3
  characters
- **THEN** the registration form is re-rendered with an error message