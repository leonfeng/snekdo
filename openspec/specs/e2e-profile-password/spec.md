## Purpose

Defines end-to-end browser tests for changing the user password in the snekdo
web frontend, verifying that users can update their password and receive
appropriate feedback for invalid input.

## Requirements

### Requirement: Change password works end-to-end

The system SHALL verify that a user can change their password.

#### Scenario: Change password successfully

- **WHEN** a user submits the password change form with the correct current
  password and a valid new password
- **THEN** the password is changed and the user is redirected to `/profile`

#### Scenario: Wrong current password shows error

- **WHEN** a user submits the password change form with an incorrect current
  password
- **THEN** the profile form is re-rendered with a "Current password is
  incorrect" error

#### Scenario: New password too short shows error

- **WHEN** a user submits the password change form with a new password shorter
  than 8 characters
- **THEN** the profile form is re-rendered with a "at least 8 characters" error

#### Scenario: Passwords do not match shows error

- **WHEN** a user submits the password change form with mismatched new password
  and confirm password
- **THEN** the profile form is re-rendered with a "Passwords do not match" error
