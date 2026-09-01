## MODIFIED Requirements

### Requirement: Complete todo via HTMX

The system SHALL allow a user to mark a todo as complete via an HTMX
button that triggers a partial page update without a full page reload.
The handler MUST load the most recent todo instance from storage before
saving. The partial HTML response SHALL include all columns present in
the full list view: ID, Title, Status, Priority, Due, Repeat, Created At,
Tags, and Category.

#### Scenario: Complete todo via HTMX

- **WHEN** a user clicks the "complete" button on a todo row
- **THEN** the server marks the todo as complete and returns a single table
  row containing all columns (ID, Title, Status, Priority, Due, Repeat,
  Created At, Tags, Category, Actions) so the row aligns with the table
  header

#### Scenario: Complete non-existent todo

- **WHEN** a user clicks "complete" on a todo that does not exist
- **THEN** the server returns a 404 response

### Requirement: Delete todo via HTMX

The system SHALL allow a user to delete a todo via an HTMX button that
triggers a partial page update without a full page reload. The partial
response SHALL include all columns present in the full list view so that
remaining rows align with the table header. When the last todo in the list
is deleted, the empty state MUST be rendered as a `<p>` element inside the
`<tbody>` (not as `outerHTML` of a `<tr>`).

#### Scenario: Delete todo via HTMX

- **WHEN** a user clicks the "delete" button on a todo row
- **THEN** the server deletes the todo and returns the remaining rows with
  all columns (ID, Title, Status, Priority, Due, Repeat, Created At, Tags,
  Category, Actions) so the table remains aligned

#### Scenario: Delete last todo shows empty state

- **WHEN** a user deletes the last remaining todo via HTMX
- **THEN** the table body displays an empty-state message without invalid HTML

#### Scenario: Delete non-existent todo

- **WHEN** a user clicks "delete" on a todo that does not exist
- **THEN** the server returns a 404 response

### Requirement: Show todo details via web UI

The system SHALL provide a page that displays the full details of a
single todo.

#### Scenario: Show todo details

- **WHEN** a user navigates to `/todos/{id}`
- **THEN** the server renders an HTML page showing the todo's ID, title,
  description, due, priority, status, repeat, tags, category, and
  created at

#### Scenario: Show non-existent todo

- **WHEN** a user navigates to `/todos/{non-existent-id}`
- **THEN** the server returns a 404 response

## ADDED Requirements

### Requirement: Confirmation page is standalone

The account deletion confirmation page SHALL NOT display the
authenticated navigation bar. After account deletion the user is
logged out, so showing nav links to protected pages is misleading.

#### Scenario: Confirmation page has no navigation

- **WHEN** a user deletes their account and is shown the confirmation
  page
- **THEN** the page displays a success message without any navigation
  links to authenticated routes

### Requirement: Confirmation page success message is styled

The confirmation page SHALL use a CSS class that is defined in the
application's stylesheet so the success message is visually distinct.

#### Scenario: Success message is styled

- **WHEN** a user views the account deletion confirmation page
- **THEN** the success message is rendered with visible styling (green
  or green-ish background, padded, bordered)
