## MODIFIED Requirements

### Requirement: Support all modifiable fields

The system SHALL allow updating all optional todo attributes: title, description, due date, priority, completed status, tags, and category.

#### Scenario: Update description
- **WHEN** user runs modify command with `--description` argument
- **THEN** system updates the description field

#### Scenario: Update due date
- **WHEN** user runs modify command with `--due` argument
- **THEN** system updates the due date field

#### Scenario: Clear due date
- **WHEN** user runs modify command with empty `--due` argument
- **THEN** system does not modify the existing due date field (empty string is treated as not provided, preserving the current value)

#### Scenario: Update priority
- **WHEN** user runs modify command with `--priority` argument
- **THEN** system updates the priority field

#### Scenario: Update completed status
- **WHEN** user runs modify command with `--completed` argument
- **THEN** system updates the completed status of the todo

#### Scenario: Clear completed status
- **WHEN** user runs modify command with `--completed false`
- **THEN** system marks the todo as not completed

#### Scenario: Update tags
- **WHEN** user runs modify command with one or more `--tag` arguments
- **THEN** system replaces the todo's tags with the given list

#### Scenario: Update category
- **WHEN** user runs modify command with `--category home`
- **THEN** system updates the todo's category to "home"

#### Scenario: Clear category
- **WHEN** user runs modify command with empty `--category` argument
- **THEN** system clears the todo's category (sets it to None)
