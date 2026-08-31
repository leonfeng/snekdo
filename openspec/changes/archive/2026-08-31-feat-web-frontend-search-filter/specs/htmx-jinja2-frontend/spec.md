## MODIFIED Requirements

### Requirement: List todos via web UI
The system SHALL provide a web page that displays todos in a table, matching the CLI list display conventions (Title, ID, Status, Priority, Due, Created At columns). The page SHALL support filtering by search query (title/description substring), status (pending/completed/all), and priority (high/medium/low) via query parameters.

#### Scenario: List page shows todos
- **WHEN** a user navigates to `/todos`
- **THEN** the server renders an HTML table listing pending todos with their ID, Title, Status, Priority, Due date, and Created At

#### Scenario: List page is empty
- **WHEN** no matching todos exist and a user navigates to `/todos`
- **THEN** the page displays a message indicating no todos are found

#### Scenario: List page with search query
- **WHEN** a user navigates to `/todos?q=buy`
- **THEN** the server renders an HTML table with only todos whose title or description contains "buy" (case-insensitive)

#### Scenario: List page with status filter
- **WHEN** a user navigates to `/todos?status=completed`
- **THEN** the server renders an HTML table with only completed todos

#### Scenario: List page with priority filter
- **WHEN** a user navigates to `/todos?priority=high`
- **THEN** the server renders an HTML table with only high-priority todos

#### Scenario: List page with combined filters
- **WHEN** a user navigates to `/todos?q=buy&status=all&priority=high`
- **THEN** the server renders an HTML table with only high-priority todos whose title or description contains "buy", regardless of completion status

#### Scenario: List page shows all statuses
- **WHEN** a user navigates to `/todos?status=all`
- **THEN** the server renders an HTML table with both pending and completed todos
