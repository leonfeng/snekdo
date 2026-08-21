## Purpose

This capability provides the web frontend for authenticated users to delete their own account.

## ADDED Requirements

### Requirement: Delete account option on profile page

The system SHALL provide a delete account option on the authenticated user's profile page.

#### Scenario: Delete account button is shown

- **WHEN** an authenticated user navigates to `/profile`
- **THEN** the page includes a "Delete account" button or link

#### Scenario: Unauthenticated access redirects to login

- **WHEN** an unauthenticated user navigates to `/profile`
- **THEN** the server redirects to `/auth/login`

### Requirement: Delete account confirmation

The system SHALL require confirmation before deleting the account.

#### Scenario: Delete account confirmation dialog

- **WHEN** a user clicks the "Delete account" button
- **THEN** the user is prompted to confirm the deletion (e.g., JavaScript `confirm()` dialog)

#### Scenario: Delete account password confirmation

- **WHEN** a user confirms the deletion
- **THEN** the user is prompted to enter their password

#### Scenario: Delete account succeeds

- **WHEN** a user confirms deletion and enters the correct password
- **THEN** the account is deleted
- **AND** the user is redirected to `/auth/login`

#### Scenario: Delete account with wrong password fails

- **WHEN** a user confirms deletion but enters an incorrect password
- **THEN** the account is not deleted
- **AND** an error message is shown
