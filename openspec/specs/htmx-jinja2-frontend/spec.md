## Purpose

Provides a browser-based todo management interface using Jinja2 for
server-side HTML templating and HTMX for interactive, partial-page updates,
served alongside the existing REST API on the same FastAPI server.

## Requirements

### Requirement: Web UI is served alongside the API

The system SHALL serve the HTMX/Jinja2 web frontend on the same FastAPI
server that hosts the REST API, so that `snekdo serve` makes both the API
and the web UI available on a single host/port.

#### Scenario: Web UI is reachable

- **WHEN** the server is started with `snekdo serve`
- **THEN** the web UI is available at the root path `/` and the API remains
  available at `/api/v1/*`

### Requirement: List todos via web UI

The system SHALL provide a web page that displays todos in a table, matching
the CLI list display conventions (Title, ID, Status, Priority, Due, Created At
columns). The page SHALL support filtering by search query
(title/description substring), status (pending/completed/all), and priority
(high/medium/low) via query parameters.

#### Scenario: List page shows todos

- **WHEN** a user navigates to `/todos`
- **THEN** the server renders an HTML table listing pending todos with their
  ID, Title, Status, Priority, Due date, and Created At

#### Scenario: List page is empty

- **WHEN** no matching todos exist and a user navigates to `/todos`
- **THEN** the page displays a message indicating no todos are found

#### Scenario: List page with search query

- **WHEN** a user navigates to `/todos?q=buy`
- **THEN** the server renders an HTML table with only todos whose title or
  description contains "buy" (case-insensitive)

#### Scenario: List page with status filter

- **WHEN** a user navigates to `/todos?status=completed`
- **THEN** the server renders an HTML table with only completed todos

#### Scenario: List page with priority filter

- **WHEN** a user navigates to `/todos?priority=high`
- **THEN** the server renders an HTML table with only high-priority todos

#### Scenario: List page with combined filters

- **WHEN** a user navigates to `/todos?q=buy&status=all&priority=high`
- **THEN** the server renders an HTML table with only high-priority todos
  whose title or description contains "buy", regardless of completion status

#### Scenario: List page shows all statuses

- **WHEN** a user navigates to `/todos?status=all`
- **THEN** the server renders an HTML table with both pending and completed
  todos

### Requirement: Add todo via web UI

The system SHALL provide a web form to add a new todo. The form includes
fields for title, description, due date, priority, repeat, tags
(comma-separated), and category. The priority field MUST only accept the
values `high`, `medium`, or `low`.

#### Scenario: Add todo form is rendered

- **WHEN** a user navigates to `/todos/add`
- **THEN** the server renders an HTML form with title, description, due,
  priority, repeat, tags, and category fields

#### Scenario: Add form renders new inputs

- **WHEN** a user visits the add page
- **THEN** the form includes a text input for `tags` (placeholder
  "work, personal") and a text input for `category` (placeholder
  "e.g., office")

#### Scenario: Add with tags and category

- **WHEN** a user submits the add form with tags "work, urgent" and
  category "office"
- **THEN** the created todo has `tags == ["work", "urgent"]` and
  `category == "office"`

#### Scenario: Add with empty tags and category

- **WHEN** a user submits the add form with empty tags and category
  fields
- **THEN** the created todo has `tags == []` and `category is None`

#### Scenario: Add trims whitespace in tags

- **WHEN** a user submits the add form with tags " work ,  urgent "
- **THEN** the created todo has `tags == ["work", "urgent"]`

#### Scenario: Add todo successfully

- **WHEN** a user submits the add form with a valid title
- **THEN** the server creates the todo and redirects to the list page

#### Scenario: Add todo with invalid data

- **WHEN** a user submits the add form with an empty title
- **THEN** the server renders the form with a validation error message

#### Scenario: Add todo with invalid priority

- **WHEN** a user submits the add form with a priority value other than
  `high`, `medium`, or `low`
- **THEN** the server renders the form with a validation error message

### Requirement: Complete todo via HTMX

The system SHALL allow a user to mark a todo as complete via an HTMX
button that triggers a partial page update without a full page reload.
The handler MUST load the most recent todo instance from storage before
saving.

#### Scenario: Complete todo via HTMX

- **WHEN** a user clicks the "complete" button on a todo row
- **THEN** the server marks the todo as complete and the page updates
  the status cell to "✓" without a full page reload

#### Scenario: Complete non-existent todo

- **WHEN** a user clicks "complete" on a todo that does not exist
- **THEN** the server returns a 404 response

### Requirement: Delete todo via HTMX

The system SHALL allow a user to delete a todo via an HTMX button that
triggers a partial page update without a full page reload. When the last
todo in the list is deleted, the empty state MUST be rendered as a `<p>`
element inside the `<tbody>` (not as `outerHTML` of a `<tr>`).

#### Scenario: Delete todo via HTMX

- **WHEN** a user clicks the "delete" button on a todo row
- **THEN** the server deletes the todo and removes the row from the
  table without a full page reload

#### Scenario: Delete last todo shows empty state

- **WHEN** a user deletes the last remaining todo via HTMX
- **THEN** the table body displays an empty-state message without invalid HTML

#### Scenario: Delete non-existent todo

- **WHEN** a user clicks "delete" on a todo that does not exist
- **THEN** the server returns a 404 response

### Requirement: Modify todo via web UI

The system SHALL provide a web form to modify an existing todo's title,
description, due date, priority, repeat, tags, and category. An empty
string value for due date MUST clear the existing due date. An empty
string value for category MUST clear the existing category. The tags
field SHALL be comma-separated; the handler SHALL split, trim, drop
empties, and dedupe while preserving order.

#### Scenario: Edit todo form is rendered

- **WHEN** a user navigates to `/todos/{id}/edit`
- **THEN** the server renders an HTML form pre-filled with the todo's
  current values, including comma-joined tags and category

#### Scenario: Edit form pre-fills tags and category

- **WHEN** a user opens the edit page for a todo with `tags=["work","home"]`
  and `category="office"`
- **THEN** the tags input contains "work, home" and the category input
  contains "office"

#### Scenario: Edit updates tags and category

- **WHEN** a user submits the edit form with new tags "urgent" and
  category "home"
- **THEN** the todo is updated to `tags == ["urgent"]` and
  `category == "home"`

#### Scenario: Modify todo successfully

- **WHEN** a user submits the edit form with updated values
- **THEN** the server updates the todo and redirects to the list page

#### Scenario: Modify non-existent todo

- **WHEN** a user navigates to `/todos/{non-existent-id}/edit`
- **THEN** the server returns a 404 response

#### Scenario: Edit todo with empty due date clears due date

- **WHEN** a user submits the edit form with an empty due date
- **THEN** the todo's due date is cleared

### Requirement: Show todo details via web UI

The system SHALL provide a page that displays the full details of a
single todo.

#### Scenario: Show todo details

- **WHEN** a user navigates to `/todos/{id}`
- **THEN** the server renders an HTML page showing the todo's ID, title,
  description, due, priority, status, and created at

#### Scenario: Show non-existent todo

- **WHEN** a user navigates to `/todos/{non-existent-id}`
- **THEN** the server returns a 404 response

### Requirement: HTMX forms include CSRF tokens

The system SHALL include a CSRF token in every state-changing form (add,
edit, complete, delete, profile update, password change, account deletion)
so that the server can validate the request.

#### Scenario: Add form includes CSRF token

- **WHEN** a user navigates to `/todos/add`
- **THEN** the form includes a hidden input field containing the CSRF token

#### Scenario: Edit form includes CSRF token

- **WHEN** a user navigates to `/todos/{id}/edit`
- **THEN** the form includes a hidden input field containing the CSRF token

#### Scenario: Delete form includes CSRF token

- **WHEN** a user views the todo list
- **THEN** each delete button includes the CSRF token (as a data attribute
  or hidden input)

### Requirement: Web forms handle validation errors as HTML

The system SHALL re-render forms with HTML validation error messages when
submission fails due to invalid input, instead of returning JSON error
responses.

#### Scenario: Add todo invalid input returns HTML

- **WHEN** a user submits the add form with invalid data
- **THEN** the server returns HTML (not JSON) with the form and error message

#### Scenario: Edit todo invalid input returns HTML

- **WHEN** a user submits the edit form with invalid data
- **THEN** the server returns HTML (not JSON) with the form and error message

### Requirement: Profile forms use valid HTMX targets

The system SHALL use HTMX targets that reference elements inside the form
container, not the form container itself, to avoid self-referential
replacement issues.

#### Scenario: Profile form targets inner container

- **WHEN** a user submits the profile update form
- **THEN** the response is swapped into a container within the form, not
  the form's own wrapper

### Requirement: Delete account handles HTMX requests

The system SHALL return HTML content (not a 302 redirect) when a
delete-account request is made via HTMX.

#### Scenario: Delete account HTMX returns HTML

- **WHEN** a user clicks "Delete account" and confirms via HTMX
- **THEN** the page updates with a confirmation message without a full
  page reload

### Requirement: HTMX is loaded without a build step

The system SHALL load HTMX via a CDN script tag in the HTML templates,
avoiding any npm or build-step dependency.

#### Scenario: HTMX script is present

- **WHEN** a user loads any web page
- **THEN** the HTML includes a script tag loading HTMX from a CDN

### Requirement: Web UI is responsive

The system SHALL render the web UI in a layout that is usable on both
desktop and mobile viewports.

#### Scenario: Responsive layout

- **WHEN** a user loads the web UI on a small viewport
- **THEN** the todo list remains readable and interactive

### Requirement: Registration page

The system SHALL provide a `/auth/register` web page that renders a
registration form.

#### Scenario: Registration form is rendered

- **WHEN** a user navigates to `/auth/register`
- **THEN** the system displays a form with `username` and `password`
  fields and a submit button

#### Scenario: Registration form submission creates account

- **WHEN** a user submits the registration form with valid credentials
- **THEN** the system creates the account and redirects to the todo list
  page

#### Scenario: Registration with invalid data shows error

- **WHEN** a user submits the registration form with invalid data
- **THEN** the system displays the form with an error message

### Requirement: Login page

The system SHALL provide a `/auth/login` web page that renders a login
form.

#### Scenario: Login form is rendered

- **WHEN** a user navigates to `/auth/login`
- **THEN** the system displays a form with `username` and `password`
  fields and a submit button

#### Scenario: Login form submission authenticates

- **WHEN** a user submits the login form with valid credentials
- **THEN** the system authenticates the user and redirects to the todo
  list page

#### Scenario: Login with invalid credentials shows error

- **WHEN** a user submits the login form with invalid credentials
- **THEN** the system displays the form with an error message

### Requirement: Unauthenticated access redirect

The system SHALL redirect unauthenticated users to the login page when
accessing todo routes.

#### Scenario: Todo route redirects to login

- **WHEN** an unauthenticated user navigates to `/todos`
- **THEN** the system redirects to `/auth/login`

#### Scenario: Auth routes are accessible without login

- **WHEN** an unauthenticated user navigates to `/auth/register` or
  `/auth/login`
- **THEN** the system displays the form without redirecting

### Requirement: Logout

The system SHALL provide a logout route that invalidates the current
session.

#### Scenario: Logout redirects to login

- **WHEN** an authenticated user clicks logout
- **THEN** the system invalidates the session and redirects to
  `/auth/login`

### Requirement: List view displays tags and category columns

The list view SHALL display a `Tags` column and a `Category` column after
`Created At`, with empty cells when a todo has no tags or category.

#### Scenario: List shows tags and category

- **WHEN** a user views the list page with a todo having tags and a
  category
- **THEN** the row displays the comma-joined tags in the Tags column and
  the category in the Category column

#### Scenario: List shows empty cells for missing tags/category

- **WHEN** a user views the list page with a todo that has no tags and no
  category
- **THEN** the Tags and Category cells are empty
