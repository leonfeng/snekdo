## Purpose

Defines end-to-end browser tests for updating the user profile (display name
and email) in the snekdo web frontend, verifying that users can update their
information and receive appropriate feedback for invalid input.

## ADDED Requirements

### Requirement: Update profile works end-to-end

The system SHALL verify that a user can update their display name and email.

#### Scenario: Update display name

- **WHEN** a user submits the profile update form with a new display name
- **THEN** the display name is updated and the user is redirected to `/profile`

#### Scenario: Update email

- **WHEN** a user submits the profile update form with a new email
- **THEN** the email is updated and the user is redirected to `/profile`

#### Scenario: Invalid email format shows error

- **WHEN** a user submits the profile update form with an invalid email
- **THEN** the profile form is re-rendered with an "Invalid email format" error