## Purpose

This capability provides CSRF token generation and validation for all web forms and state-changing requests in the snekdo HTMX/Jinja2 frontend, protecting against cross-site request forgery attacks.

## ADDED Requirements

### Requirement: CSRF token is generated per session

The system SHALL generate a cryptographically random CSRF token when a user session is created and store it in the session.

#### Scenario: Token is generated on login

- **WHEN** a user logs in successfully
- **THEN** a CSRF token is generated and stored in the session

#### Scenario: Token is unique per session

- **WHEN** two different users log in
- **THEN** each session has a different CSRF token

### Requirement: CSRF token is included in forms

The system SHALL make the CSRF token available to all web templates so it can be included as a hidden input in every state-changing form.

#### Scenario: Token is available in templates

- **WHEN** a web page renders a form
- **THEN** the template can access the CSRF token

### Requirement: CSRF token is validated on state-changing requests

The system SHALL validate the CSRF token on every POST, PUT, and DELETE request that modifies state.

#### Scenario: Valid token accepted

- **WHEN** a form submission includes a valid CSRF token
- **THEN** the request is processed normally

#### Scenario: Missing token rejected

- **WHEN** a state-changing request is missing the CSRF token
- **THEN** the server returns a 403 Forbidden response

#### Scenario: Invalid token rejected

- **WHEN** a state-changing request includes an invalid CSRF token
- **THEN** the server returns a 403 Forbidden response

#### Scenario: HTMX requests are validated

- **WHEN** an HTMX request modifies state without a valid CSRF token
- **THEN** the server returns a 403 Forbidden response

### Requirement: CSRF token is rotated on login

The system SHALL rotate the CSRF token when a user logs in to prevent session fixation attacks.

#### Scenario: Token rotates on login

- **WHEN** a user logs in
- **THEN** the previous CSRF token is replaced with a new one

### Requirement: CSRF token is invalidated on logout

The system SHALL invalidate the CSRF token when a user logs out.

#### Scenario: Token invalidated on logout

- **WHEN** a user logs out
- **THEN** the CSRF token is removed from the session