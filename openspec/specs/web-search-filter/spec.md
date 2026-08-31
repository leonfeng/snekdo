# Spec: web-search-filter

## Purpose

Adds client-side search and server-side filtering to the web frontend, allowing users to filter todos by text query (title/description), status, and priority with HTMX-driven partial page updates.

## Requirements

### Requirement: Text search filter
The web list page SHALL support a search input that filters todos by a case-insensitive substring match on the title and description fields.

#### Scenario: Search by title substring
- **WHEN** the user types "buy" in the search box and the list contains todos "Buy groceries" and "Buy milk" and "Write report"
- **THEN** only the todos whose title or description contains "buy" (case-insensitive) are displayed

#### Scenario: Search matches description
- **WHEN** the user types "urgent" in the search box and a todo has title "Weekly task" but description "This is urgent"
- **THEN** that todo is displayed in the results

#### Scenario: Empty search shows all
- **WHEN** the search box is empty or the search parameter is omitted
- **THEN** all todos matching the other active filters are displayed

#### Scenario: No search results
- **WHEN** the user types a query that matches no todos
- **THEN** the list displays the "No todos found" empty state message

### Requirement: Status filter
The web list page SHALL support a status filter with options: All, Pending, Completed.

#### Scenario: Filter by pending
- **WHEN** the user selects "Pending" in the status dropdown
- **THEN** only todos with completed=false are displayed

#### Scenario: Filter by completed
- **WHEN** the user selects "Completed" in the status dropdown
- **THEN** only todos with completed=true are displayed

#### Scenario: Filter by all
- **WHEN** the user selects "All" in the status dropdown
- **THEN** both pending and completed todos are displayed

#### Scenario: Default status is pending
- **WHEN** the user navigates to the list page without specifying a status
- **THEN** only pending todos are displayed (matching existing CLI behavior)

### Requirement: Priority filter
The web list page SHALL support a priority filter with options: All, High, Medium, Low.

#### Scenario: Filter by high priority
- **WHEN** the user selects "High" in the priority dropdown
- **THEN** only todos with priority "high" are displayed

#### Scenario: Filter by low priority
- **WHEN** the user selects "Low" in the priority dropdown
- **THEN** only todos with priority "low" are displayed

#### Scenario: All priority shows everything
- **WHEN** the user selects "All" in the priority dropdown
- **THEN** todos of all priorities are displayed (subject to other active filters)

### Requirement: Filters combine with AND semantics
When multiple filters are active simultaneously, the system SHALL apply all filters conjunctively (AND logic).

#### Scenario: Search and status combined
- **WHEN** the user has search query "buy" and status set to "Completed"
- **THEN** only completed todos whose title or description contains "buy" are displayed

#### Scenario: Search, status, and priority combined
- **WHEN** the user has search query "office", status "All", and priority "High"
- **THEN** only high-priority todos whose title or description contains "office" are displayed regardless of completion status

### Requirement: Filter state persists in URL
The filter selections SHALL be reflected in the URL query parameters so that the filtered state is shareable and preserved on page refresh.

#### Scenario: URL reflects active filters
- **WHEN** the user applies search "buy", status "pending", and priority "high"
- **THEN** the URL becomes `/todos?q=buy&status=pending&priority=high`

#### Scenario: Page refresh preserves filters
- **WHEN** the user refreshes the page with active filter query parameters in the URL
- **THEN** the same filtered results are displayed

### Requirement: Filter bar uses HTMX for partial updates
Changes to the search input, status dropdown, or priority dropdown SHALL trigger an HTMX GET request that updates only the todo table portion of the page, without a full page reload.

#### Scenario: Search triggers partial update
- **WHEN** the user types in the search box (with a debounce delay of ~300ms)
- **THEN** an HTMX GET request is sent to `/todos` with the `q` parameter and the table body is updated without a full page reload

#### Scenario: Status change triggers partial update
- **WHEN** the user selects a different option in the status dropdown
- **THEN** an HTMX GET request is sent to `/todos` with the `status` parameter and the table body is updated without a full page reload

#### Scenario: Priority change triggers partial update
- **WHEN** the user selects a different option in the priority dropdown
- **THEN** an HTMX GET request is sent to `/todos` with the `priority` parameter and the table body is updated without a full page reload

### Requirement: Filter bar preserves existing list columns
The filter bar SHALL be rendered above the todo table without altering the existing table columns (ID, Title, Status, Priority, Due, Repeat, Created At, Tags, Category, Actions).

#### Scenario: Filter bar does not affect table structure
- **WHEN** the user applies any combination of filters
- **THEN** the todo table retains all existing columns with the same widths and formatting
