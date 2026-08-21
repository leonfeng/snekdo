## Purpose

This capability provides the HTTP client method for programmatic account deletion.

## ADDED Requirements

### Requirement: API client delete_account method

The system SHALL provide a `delete_account(password, credentials_path)` method on `ServerHttpClient` that deletes the current user's account.

#### Scenario: Client delete account succeeds

- **WHEN** `ServerHttpClient.delete_account(password=...)` is called with a valid password
- **THEN** the method returns the message response dict
- **AND** the account is deleted on the server

#### Scenario: Client delete account with wrong password fails

- **WHEN** `ServerHttpClient.delete_account(password=...)` is called with an incorrect password
- **THEN** the method raises `AuthenticationError`

#### Scenario: Client delete account without credentials fails

- **WHEN** `ServerHttpClient.delete_account()` is called without stored credentials
- **THEN** the method raises `AuthenticationError`
