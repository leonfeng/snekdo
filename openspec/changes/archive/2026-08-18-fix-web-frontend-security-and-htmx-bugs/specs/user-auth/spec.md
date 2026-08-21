## MODIFIED Requirements

### Requirement: Authentication endpoint for web frontend

The system SHALL provide web pages for registration and login via the Jinja2 frontend. Login and registration forms MUST validate input manually and re-render the form with HTML error messages on failure, instead of returning JSON validation errors.

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

### Requirement: Logout

The system SHALL provide a logout endpoint that invalidates the user session. The logout endpoint MUST use the HTTP POST method so that it is not cacheable or CSRF-able.

#### Scenario: Logout redirects to login

- **WHEN** a logged-in user clicks the logout link
- **THEN** the session is invalidated and the user is redirected to `/auth/login`

#### Scenario: Logout requires POST

- **WHEN** a user sends a GET request to the logout endpoint
- **THEN** the server returns a 405 Method Not Allowed response

#### Scenario: Logout invalidates CSRF token

- **WHEN** a user logs out
- **THEN** the CSRF token is also invalidated

### Requirement: Authentication endpoint for CLI

The system SHALL provide a way for the CLI to obtain an access token for use with the sync command.

#### Scenario: CLI login obtains token

- **WHEN** a user runs `snekdo login` with valid credentials
- **THEN** the system stores the access token for subsequent commands
