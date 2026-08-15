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

The system SHALL provide a web page that displays all pending todos in a
table, matching the CLI list display conventions (Title, ID, Status,
Priority, Due, Created At columns).

#### Scenario: List page shows todos

- **WHEN** a user navigates to `/todos`
- **THEN** the server renders an HTML table listing all pending todos with
  their ID, Title, Status, Priority, Due date, and Created At

#### Scenario: List page is empty

- **WHEN** no todos exist and a user navigates to `/todos`
- **THEN** the page displays a message indicating no todos are found

### Requirement: Add todo via web UI

The system SHALL provide a web form to add a new todo. The form includes
fields for title, description, due date, and priority.

#### Scenario: Add todo form is rendered

- **WHEN** a user navigates to `/todos/add`
- **THEN** the server renders an HTML form with title, description, due,
  and priority fields

#### Scenario: Add todo successfully

- **WHEN** a user submits the add form with a valid title
- **THEN** the server creates the todo and redirects to the list page

#### Scenario: Add todo with invalid data

- **WHEN** a user submits the add form with an empty title
- **THEN** the server renders the form with a validation error message

### Requirement: Complete todo via HTMX

The system SHALL allow a user to mark a todo as complete via an HTMX
button that triggers a partial page update without a full page reload.

#### Scenario: Complete todo via HTMX

- **WHEN** a user clicks the "complete" button on a todo row
- **THEN** the server marks the todo as complete and the page updates
  the status cell to "✓" without a full page reload

#### Scenario: Complete non-existent todo

- **WHEN** a user clicks "complete" on a todo that does not exist
- **THEN** the server returns a 404 response

### Requirement: Delete todo via HTMX

The system SHALL allow a user to delete a todo via an HTMX button that
triggers a partial page update without a full page reload.

#### Scenario: Delete todo via HTMX

- **WHEN** a user clicks the "delete" button on a todo row
- **THEN** the server deletes the todo and removes the row from the
  table without a full page reload

#### Scenario: Delete non-existent todo

- **WHEN** a user clicks "delete" on a todo that does not exist
- **THEN** the server returns a 404 response

### Requirement: Modify todo via web UI

The system SHALL provide a web form to modify an existing todo's title,
description, due date, and priority.

#### Scenario: Edit todo form is rendered

- **WHEN** a user navigates to `/todos/{id}/edit`
- **THEN** the server renders an HTML form pre-filled with the todo's
  current values

#### Scenario: Modify todo successfully

- **WHEN** a user submits the edit form with updated values
- **THEN** the server updates the todo and redirects to the list page

#### Scenario: Modify non-existent todo

- **WHEN** a user navigates to `/todos/{non-existent-id}/edit`
- **THEN** the server returns a 404 response

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
