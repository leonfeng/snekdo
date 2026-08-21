## Delta for existing capability: user-auth

## MODIFIED Requirements

### Requirement: Password storage security

The system SHALL store user passwords as salted hashes and never store or log plaintext passwords. Secret configuration (JWT signing key, secret key) MUST be sourced from an environment variable with a random per-deployment value as the default, and MUST NOT fall back to a hardcoded static value.

#### Scenario: Plaintext password is never stored

- **WHEN** a user registers
- **THEN** the stored user record contains only a hash, not the plaintext password

#### Scenario: Hashing algorithm is used

- **WHEN** a user registers or logs in
- **THEN** the system uses a recognized password hashing library (e.g., passlib/bcrypt)

#### Scenario: No hardcoded default secret

- **WHEN** the server starts without an explicit secret-configured environment variable
- **THEN** the system generates a random per-process signing key rather than using a static hardcoded secret, and the startup logs contain no user password or plaintext credential value

#### Scenario: Plaintext passwords never appear in logs

- **WHEN** a user registers or logs in
- **THEN** the server logs at most a redacted identifier (e.g., the username) and never the password value

### Requirement: Authentication endpoint for web frontend

The system SHALL provide web pages for registration and login via the Jinja2 frontend. The web login form MUST require both a username and a password to be present before attempting authentication.

#### Scenario: Registration page is accessible

- **WHEN** a user navigates to `/auth/register`
- **THEN** the system renders a registration form

#### Scenario: Login page is accessible

- **WHEN** a user navigates to `/auth/login`
- **THEN** the system renders a login form

#### Scenario: Login with invalid input re-renders form

- **WHEN** a user submits the login form with an empty username or password
- **THEN** the login form is re-rendered with an HTML error message

#### Scenario: Registration with invalid input re-renders form

- **WHEN** a user submits the registration form with an invalid username or password
- **THEN** the registration form is re-rendered with an HTML error message