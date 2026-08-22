## MODIFIED Requirements

### Requirement: List todos via web UI

The system SHALL provide a web page that displays all pending todos in a table, matching the CLI list display conventions (Title, ID, Status, Priority, Due, Created At columns), and includes a collapsible section for completed todos.

#### Scenario: List page shows todos with collapsible completed section

- **WHEN** a user navigates to `/todos`
- **THEN** the server renders an HTML table listing all pending todos with their ID, Title, Status, Priority, Due date, and Created At, along with a collapsible heading showing the count of completed todos

#### Scenario: Collapsible heading appears on list page

- **WHEN** a user navigates to `/todos` and there are completed todos
- **THEN** the page includes a collapsible element displaying `"{n} completed todos"` with a caret icon
