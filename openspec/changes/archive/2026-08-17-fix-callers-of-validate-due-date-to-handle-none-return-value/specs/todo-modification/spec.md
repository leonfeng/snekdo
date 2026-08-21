## MODIFIED Requirements

### Requirement: Support all modifiable fields

The system SHALL allow updating all optional todo attributes: title, description, and due date.

#### Scenario: Update description
- **WHEN** user runs modify command with `--description` argument
- **THEN** system updates the description field

#### Scenario: Update due date
- **WHEN** user runs modify command with `--due` argument
- **THEN** system updates the due date field

#### Scenario: Clear due date
- **WHEN** user runs modify command with empty `--due` argument
- **THEN** system does not modify the existing due date field (empty string is treated as not provided, preserving the current value)
