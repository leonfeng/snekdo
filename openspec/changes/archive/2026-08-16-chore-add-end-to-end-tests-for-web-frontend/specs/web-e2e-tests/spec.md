## Purpose

Defines end-to-end (E2E) browser tests for the snekdo HTMX/Jinja2 web frontend,
verifying that the full user journeys — registration, login, logout, todo CRUD,
and profile management — work correctly in a real browser via Playwright.

## ADDED Requirements

### Requirement: E2E test harness boots a test server

The system SHALL provide an E2E test harness that starts a temporary FastAPI
test server and a Playwright browser context so tests can exercise the web UI
end-to-end without manual setup.

#### Scenario: Test server is reachable

- **WHEN** the E2E test harness is initialized
- **THEN** a FastAPI app with web routes is running on a local port and is
  reachable via `http://127.0.0.1:<port>`

#### Scenario: Browser context is available

- **WHEN** the E2E test harness is initialized
- **THEN** a Playwright browser context is available for navigation and
  interaction

### Requirement: Registration flow works end-to-end

The system SHALL verify that a new user can register, log in, and is redirected
to the todo list.

#### Scenario: Registration form is submitted

- **WHEN** a user fills in a username and password on `/auth/register` and
  submits the form
- **THEN** the account is created and the user is redirected to `/todos`

#### Scenario: Registration with missing fields shows error

- **WHEN** a user submits the registration form with an empty username
- **THEN** the registration form is re-rendered with an error message

### Requirement: Login flow works end-to-end

The system SHALL verify that an existing user can log in and is redirected to
the todo list.

#### Scenario: Login with valid credentials

- **WHEN** a user enters a valid username and password on `/auth/login` and
  submits
- **THEN** the user is authenticated and redirected to `/todos`

#### Scenario: Login with invalid credentials

- **WHEN** a user enters an invalid username or password
- **THEN** the login form is re-rendered with an error message

### Requirement: Logout works end-to-end

The system SHALL verify that a logged-in user can log out and is redirected to
the login page.

#### Scenario: Logout redirects to login

- **WHEN** a logged-in user clicks the logout link
- **THEN** the session is invalidated and the user is redirected to `/auth/login`

### Requirement: Todo list page works end-to-end

The system SHALL verify that the todo list page displays pending todos and
handles an empty list.

#### Scenario: Empty list shows placeholder

- **WHEN** a logged-in user navigates to `/todos` with no todos
- **THEN** the page displays a "No todos found" message

#### Scenario: List shows todo rows

- **WHEN** a logged-in user navigates to `/todos` with pending todos
- **THEN** the page displays a table with rows for each pending todo

### Requirement: Add todo works end-to-end

The system SHALL verify that a user can add a new todo from the web form.

#### Scenario: Add todo successfully

- **WHEN** a user fills in a title on `/todos/add` and submits
- **THEN** the todo is created and the user is redirected to `/todos`

#### Scenario: Add todo with empty title shows error

- **WHEN** a user submits the add form with an empty title
- **THEN** the form is re-rendered with a "Title is required" error

### Requirement: Edit todo works end-to-end

The system SHALL verify that a user can edit an existing todo.

#### Scenario: Edit form pre-fills values

- **WHEN** a user navigates to `/todos/{id}/edit`
- **THEN** the form is pre-filled with the todo's current title, description,
  due date, and priority

#### Scenario: Edit todo successfully

- **WHEN** a user submits the edit form with updated values
- **THEN** the todo is updated and the user is redirected to `/todos`

#### Scenario: Edit todo with empty title shows error

- **WHEN** a user submits the edit form with an empty title
- **THEN** the form is re-rendered with a "Title is required" error

### Requirement: Complete todo works end-to-end

The system SHALL verify that a user can mark a todo as complete via HTMX.

#### Scenario: Complete todo via HTMX updates row

- **WHEN** a user clicks the complete button on a todo row
- **THEN** the row updates to show the completed status without a full page
  reload

#### Scenario: Complete todo via redirect

- **WHEN** a user clicks the complete button without HTMX
- **THEN** the user is redirected to `/todos`

### Requirement: Delete todo works end-to-end

The system SHALL verify that a user can delete a todo.

#### Scenario: Delete todo via HTMX removes row

- **WHEN** a user clicks the delete button on a todo row
- **THEN** the row is removed from the table without a full page reload

#### Scenario: Delete todo via redirect

- **WHEN** a user clicks the delete button without HTMX
- **THEN** the user is redirected to `/todos`

### Requirement: Show todo details works end-to-end

The system SHALL verify that a user can view the details of a single todo.

#### Scenario: Show todo details page

- **WHEN** a user navigates to `/todos/{id}`
- **THEN** the page displays the todo's title, description, due date, priority,
  status, and created at

#### Scenario: Non-existent todo shows 404

- **WHEN** a user navigates to `/todos/nonexistent-id`
- **THEN** the server returns a 404 response

### Requirement: Profile page works end-to-end

The system SHALL verify that a logged-in user can view their profile.

#### Scenario: Profile page renders

- **WHEN** a logged-in user navigates to `/profile`
- **THEN** the page displays the user's username, display name, email, and
  created at

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

### Requirement: Change password works end-to-end

The system SHALL verify that a user can change their password.

#### Scenario: Change password successfully

- **WHEN** a user submits the password change form with the correct current
  password and a valid new password
- **THEN** the password is changed and the user is redirected to `/profile`

#### Scenario: Wrong current password shows error

- **WHEN** a user submits the password change form with an incorrect current
  password
- **THEN** the profile form is re-rendered with a "Current password is
  incorrect" error

#### Scenario: New password too short shows error

- **WHEN** a user submits the password change form with a new password shorter
  than 8 characters
- **THEN** the profile form is re-rendered with a "at least 8 characters" error

#### Scenario: Passwords do not match shows error

- **WHEN** a user submits the password change form with mismatched new password
  and confirm password
- **THEN** the profile form is re-rendered with a "Passwords do not match" error
