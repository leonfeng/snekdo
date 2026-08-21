## Purpose

This capability provides authenticated users with a web-based profile page where they can view their account information, update their display name and email, and change their password through the Jinja2/HTMX frontend.

## Requirements

### Requirement: Profile page is accessible

The system SHALL provide a `GET /profile` route that displays the authenticated user's profile page.

#### Scenario: Profile page is rendered

- **WHEN** an authenticated user navigates to `/profile`
- **THEN** the server renders an HTML page showing the user's `username`, `display_name`, `email`, and `created_at`

#### Scenario: Unauthenticated access redirects to login

- **WHEN** an unauthenticated user navigates to `/profile`
- **THEN** the server redirects to `/auth/login`

### Requirement: Display profile information

The system SHALL display the authenticated user's profile information on the profile page.

#### Scenario: Profile information is shown

- **WHEN** a user visits `/profile`
- **THEN** the page displays the user's username, display name, email, and account creation timestamp

### Requirement: Update display name and email

The system SHALL allow the authenticated user to update their display name and/or email through a web form.

#### Scenario: Update display name succeeds

- **WHEN** a user submits the profile form with a new `display_name`
- **THEN** the server updates the user's display name and the page shows the updated value

#### Scenario: Update email succeeds

- **WHEN** a user submits the profile form with a new `email`
- **THEN** the server updates the user's email and the page shows the updated value

#### Scenario: Update both fields succeeds

- **WHEN** a user submits the profile form with both `display_name` and `email`
- **THEN** the server updates both fields and the page shows the updated values

#### Scenario: Update with invalid email format

- **WHEN** a user submits the profile form with an invalid `email` format
- **THEN** the page shows a validation error message

#### Scenario: Empty string clears field

- **WHEN** a user submits the profile form with `display_name` set to an empty string `""`
- **THEN** the server clears the display name (sets it to `null` or empty)

### Requirement: Change password

The system SHALL allow the authenticated user to change their password through a web form.

#### Scenario: Password change form is shown

- **WHEN** a user navigates to `/profile`
- **THEN** the page includes a password change form with `current_password`, `new_password`, and `confirm_password` fields

#### Scenario: Password change succeeds

- **WHEN** a user submits the password change form with valid `current_password`, `new_password`, and `confirm_password` that match
- **THEN** the server updates the password and displays a success message

#### Scenario: Current password is wrong

- **WHEN** a user submits the password change form with an incorrect `current_password`
- **THEN** the page shows an authentication error message

#### Scenario: New password too short

- **WHEN** a user submits the password change form with a `new_password` shorter than 8 characters
- **THEN** the page shows a validation error message

#### Scenario: New password does not match confirmation

- **WHEN** a user submits the password change form with `new_password` and `confirm_password` that do not match
- **THEN** the page shows a validation error message

### Requirement: Profile page uses HTMX

The system SHALL use HTMX for partial page updates when updating the profile, avoiding full page reloads where possible.

#### Scenario: Profile update is partial

- **WHEN** a user submits the profile update form
- **THEN** the page updates the displayed profile information without a full page reload

### Requirement: Profile isolation

The system SHALL ensure that a user can only view and modify their own profile.

#### Scenario: User cannot view another user's profile

- **WHEN** an authenticated user tries to access `/profile` using a token for a different user
- **THEN** the server returns a 404 or redirects to the user's own profile
