## ADDED Requirements

### Requirement: Registration page

The system SHALL provide a `/auth/register` web page that renders a registration form.

#### Scenario: Registration form is rendered

- **WHEN** a user navigates to `/auth/register`
- **THEN** the system displays a form with `username` and `password` fields and a submit button

#### Scenario: Registration form submission creates account

- **WHEN** a user submits the registration form with valid credentials
- **THEN** the system creates the account and redirects to the todo list page

#### Scenario: Registration with invalid data shows error

- **WHEN** a user submits the registration form with invalid data
- **THEN** the system displays the form with an error message

### Requirement: Login page

The system SHALL provide a `/auth/login` web page that renders a login form.

#### Scenario: Login form is rendered

- **WHEN** a user navigates to `/auth/login`
- **THEN** the system displays a form with `username` and `password` fields and a submit button

#### Scenario: Login form submission authenticates

- **WHEN** a user submits the login form with valid credentials
- **THEN** the system authenticates the user and redirects to the todo list page

#### Scenario: Login with invalid credentials shows error

- **WHEN** a user submits the login form with invalid credentials
- **THEN** the system displays the form with an error message

### Requirement: Unauthenticated access redirect

The system SHALL redirect unauthenticated users to the login page when accessing todo routes.

#### Scenario: Todo route redirects to login

- **WHEN** an unauthenticated user navigates to `/todos`
- **THEN** the system redirects to `/auth/login`

#### Scenario: Auth routes are accessible without login

- **WHEN** an unauthenticated user navigates to `/auth/register` or `/auth/login`
- **THEN** the system displays the form without redirecting

### Requirement: Logout

The system SHALL provide a logout route that invalidates the current session.

#### Scenario: Logout redirects to login

- **WHEN** an authenticated user clicks logout
- **THEN** the system invalidates the session and redirects to `/auth/login`
