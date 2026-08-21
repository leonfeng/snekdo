## Delta for existing capability: htmx-jinja2-frontend

## MODIFIED Requirements

### Requirement: Delete todo via HTMX

The system SHALL allow a user to delete a todo via an HTMX button that triggers a partial page update without a full page reload. When the last todo in the list is deleted, the empty state MUST be rendered as a `<p>` element inside the `<tbody>` (not as `outerHTML` of a `<tr>`). After any row removal, the remaining rows MUST keep their data-attributes and HTMX wiring intact.

#### Scenario: Delete todo via HTMX

- **WHEN** a user clicks the "delete" button on a todo row
- **THEN** the server deletes the todo and removes the row from the table without a full page reload

#### Scenario: Delete last todo shows empty state

- **WHEN** a user deletes the last remaining todo via HTMX
- **THEN** the table body displays an empty-state message without invalid HTML

#### Scenario: Delete non-existent todo

- **WHEN** a user clicks "delete" on a todo that does not exist
- **THEN** the server returns a 404 response

#### Scenario: Remaining rows stay interactive after delete

- **WHEN** a user deletes one row from a list containing multiple rows via HTMX
- **THEN** the remaining rows still update correctly on subsequent complete/delete interactions

### Requirement: Complete todo via HTMX

The system SHALL allow a user to mark a todo as complete via an HTMX button that triggers a partial page update without a full page reload. The handler MUST load the most recent todo instance from storage before saving, and the updated row MUST reflect the completed status in the status cell.

#### Scenario: Complete todo via HTMX

- **WHEN** a user clicks the "complete" button on a todo row
- **THEN** the server marks the todo as complete and the page updates the status cell to "✓" without a full page reload

#### Scenario: Complete non-existent todo

- **WHEN** a user clicks "complete" on a todo that does not exist
- **THEN** the server returns a 404 response

#### Scenario: Row re-render preserves list structure

- **WHEN** a user completes a todo via HTMX
- **THEN** the swapped row fragment uses the list row template so the table structure and sibling rows remain valid

### Requirement: Profile forms use valid HTMX targets

The system SHALL use HTMX targets that reference elements inside the form container, not the form container itself, to avoid self-referential replacement issues, for both profile update and password change forms.

#### Scenario: Profile form targets inner container

- **WHEN** a user submits the profile update form
- **THEN** the response is swapped into a container within the form, not the form's own wrapper

#### Scenario: Password change form targets inner container

- **WHEN** a user submits the password change form
- **THEN** the response is swapped into a container within the form, not the form's own wrapper

### Requirement: Delete account handles HTMX requests

The system SHALL return HTML content (not a 302 redirect) when a delete-account or password-change request is made via HTMX, so the page updates in place.

#### Scenario: Delete account HTMX returns HTML

- **WHEN** a user clicks "Delete account" and confirms via HTMX
- **THEN** the page updates with a confirmation message without a full page reload

#### Scenario: Password change HTMX returns HTML

- **WHEN** a user submits the password change form via HTMX
- **THEN** the response is HTML content that updates the form area without a full page reload