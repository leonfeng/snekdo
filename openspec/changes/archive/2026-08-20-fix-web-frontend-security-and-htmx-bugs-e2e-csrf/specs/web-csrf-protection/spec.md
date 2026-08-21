## Purpose

Protects the HTML web frontend from cross-site request forgery by issuing per-session CSRF tokens and validating them on every state-changing web endpoint, so that requests from other origins cannot perform actions as an authenticated user.

## ADDED Requirements

### Requirement: CSRF token issuance

The system SHALL issue a unique CSRF token per web session on the first state-changing page render or session creation, and provide it to the client for embedding in forms.

#### Scenario: Token is generated on session creation

- **WHEN** an unauthenticated browser opens any authenticated web page for the first time
- **THEN** the server generates a cryptographically random token and stores it in the session

#### Scenario: Token value is stable within a session

- **WHEN** an authenticated client renders two consecutive pages in the same session
- **THEN** the CSRF token presented to the client is identical across both renders

#### Scenario: Token is unique across sessions

- **WHEN** two different browser sessions are created on the same server
- **THEN** each session is issued a distinct CSRF token

### Requirement: CSRF token exposure to forms

The system SHALL expose the session's CSRF token to the client in a form-safe way for every state-changing page render.

#### Scenario: State-changing forms include the token

- **WHEN** the server renders a page containing a state-changing form (add, edit, complete, delete, profile update, password change, account deletion)
- **THEN** each such form includes a hidden input carrying the session's CSRF token

#### Scenario: Read-only pages do not require the token

- **WHEN** the server renders a read-only page (list, show)
- **THEN** the page does not require a CSRF token from the client

### Requirement: CSRF validation on state-changing requests

The system SHALL reject state-changing web requests whose supplied CSRF token does not match the session's token.

#### Scenario: Valid token is accepted

- **WHEN** a state-changing web request is submitted with a CSRF token that matches the session token
- **THEN** the server processes the request normally

#### Scenario: Missing token is rejected

- **WHEN** a state-changing web request is submitted without any CSRF token
- **THEN** the server rejects the request with a 403 response and performs no data mutation

#### Scenario: Mismatched token is rejected

- **WHEN** a state-changing web request is submitted with a CSRF token that does not match the session token
- **THEN** the server rejects the request with a 403 response and performs no data mutation

#### Scenario: Validation does not mutate state

- **WHEN** a state-changing request fails CSRF validation
- **THEN** no todo, profile, or account record is created, modified, or deleted

### Requirement: CSRF token invalidated on logout

The system SHALL invalidate the session's CSRF token when the user logs out, so the token cannot be reused after the session ends.

#### Scenario: Token is unusable after logout

- **WHEN** a user logs out and then resubmits a state-changing request with the pre-logout token
- **THEN** the server rejects the request

### Requirement: CSRF does not affect the REST API

The system SHALL enforce CSRF validation only on HTML web endpoints, leaving the JSON REST API and HTMX JSON paths unaffected.

#### Scenario: REST API requires no CSRF token

- **WHEN** a client calls `POST /api/v1/todos` with a valid JWT and no CSRF token
- **THEN** the server processes the request normally

#### Scenario: HTMX JSON requests are not CSRF-gated

- **WHEN** an HTMX request to a state-changing endpoint is submitted via JSON (with an `HX-Request` header)
- **THEN** the request is handled by the normal authentication path and is not rejected for a missing CSRF form field