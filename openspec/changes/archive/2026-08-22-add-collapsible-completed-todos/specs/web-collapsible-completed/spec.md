## ADDED Requirements

### Requirement: Collapsible completed todos UI element

The system SHALL provide a collapsible UI element in the web todo list that displays the count of completed todos in the heading and allows expanding/collapsing to show/hide the list of completed todo items.

#### Scenario: Collapsible heading shows completed count and caret icon

- **WHEN** the user navigates to the todo list page
- **THEN** the heading displays `"{n} completed todos"` where `{n}` is the actual count of completed todo items, along with a caret icon indicating expand/collapse state

#### Scenario: Collapsible expands to show completed todos

- **WHEN** the user clicks the collapsible heading while it is collapsed
- **THEN** the collapsible expands and displays the list of completed todo items below the heading

#### Scenario: Collapsible contracts to hide completed todos

- **WHEN** the user clicks the collapsible heading while it is expanded
- **THEN** the collapsible contracts and hides the list of completed todo items

#### Scenario: Completed todos are displayed in the expanded list

- **WHEN** the collapsible is expanded
- **THEN** the list displays each completed todo item with its title, ID, and other relevant details

### Requirement: Caret icon indicates expand/collapse state

The system SHALL display a caret icon next to the completed todos heading that rotates or changes to indicate whether the collapsible is currently expanded or collapsed.

#### Scenario: Caret icon reflects collapsed state

- **WHEN** the collapsible is in its collapsed state
- **THEN** the caret icon indicates a collapsed/closed state (e.g., downward-facing caret)

#### Scenario: Caret icon reflects expanded state

- **WHEN** the collapsible is in its expanded state
- **THEN** the caret icon indicates an expanded/open state (e.g., upward-facing caret)
