## ADDED Requirements

### Requirement: Invalid sort field returns a descriptive error

The system SHALL reject invalid `--sort` values with a non-zero exit code and an error message that lists the valid sort fields.

#### Scenario: Invalid sort field is rejected

- **WHEN** user runs `list --sort invalid_field`
- **THEN** system displays an error message containing the valid sort fields (`created_at`, `title`, `priority`, `completed`) and returns a non-zero exit code

#### Scenario: Invalid sort field with --reverse

- **WHEN** user runs `list --sort invalid_field --reverse`
- **THEN** system displays an error message containing the valid sort fields and returns a non-zero exit code

## MODIFIED Requirements

### Requirement: Handle invalid sort field

The system SHALL reject invalid sort field values with an error message and a non-zero exit code instead of silently falling back to a default sort.

#### Scenario: Invalid sort field

- **WHEN** user runs `list --sort invalid_field`
- **THEN** system displays an error message and returns a non-zero exit code

#### Scenario: Invalid sort field with other valid flags

- **WHEN** user runs `list --status all --sort invalid_field --limit 5`
- **THEN** system displays an error message and returns a non-zero exit code without listing todos
