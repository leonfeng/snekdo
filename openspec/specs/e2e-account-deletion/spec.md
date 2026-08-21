## Purpose

This capability provides end-to-end test scenarios for account deletion via the web frontend, covering the full user journey from clicking the delete button to being redirected after successful deletion.

## Requirements

### Requirement: Delete account via web frontend

The system SHALL allow an authenticated user to delete their account through the web profile page.

#### Scenario: Delete account button is visible on profile page

- **WHEN** an authenticated user navigates to `/profile`
- **THEN** the page contains a "Delete account" button or link

#### Scenario: Delete account confirmation dialog

- **WHEN** a user clicks the "Delete account" button
- **THEN** a JavaScript `confirm()` dialog is shown

#### Scenario: Delete account with correct password succeeds

- **WHEN** a user confirms the deletion and enters the correct password
- **THEN** the account is deleted
- **AND** the user is redirected to `/auth/login`

#### Scenario: Delete account with wrong password fails

- **WHEN** a user confirms deletion but enters an incorrect password
- **THEN** the account is not deleted
- **AND** an error message is shown on the profile page

#### Scenario: Delete account cancels on dismiss

- **WHEN** a user clicks "Delete account" and dismisses the confirmation dialog
- **THEN** the profile page remains unchanged

### Requirement: Account deletion cascades to todos

The system SHALL delete all todos belonging to the deleted user when the account is deleted.

#### Scenario: All user todos are deleted

- **WHEN** an authenticated user deletes their account via the web frontend
- **THEN** all todos belonging to that user are removed from the todo storage

#### Scenario: Other users' todos are preserved

- **WHEN** an authenticated user deletes their own account
- **THEN** todos belonging to other users remain in the todo storage

### Requirement: Token invalidation after deletion

The system SHALL ensure that a deleted user's session token is no longer valid.

#### Scenario: Deleted user cannot access profile

- **WHEN** a deleted user's token is used to access `/profile`
- **THEN** the server redirects to `/auth/login`
