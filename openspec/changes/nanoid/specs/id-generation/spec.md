## Purpose

This capability defines how todo item IDs are generated. The system SHALL use nanoid to generate short, URL-friendly, unique IDs instead of UUIDs.

## Requirements

### Requirement: Generate nanoid-based IDs

The system SHALL use nanoid to generate unique IDs for new todo items.

#### Scenario: Generate ID on todo creation

- **WHEN** user creates a new todo item
- **THEN** system generates a unique ID using nanoid (21-character random string by default)

#### Scenario: ID format

- **WHEN** a todo ID is generated
- **THEN** system produces a URL-safe, random string (alphanumeric characters only, no hyphens or special characters)

### Requirement: Use nanoid in ID generation

The system SHALL import and use nanoid from the `nanoid` package for all ID generation.

#### Scenario: Import nanoid

- **WHEN** the application needs to generate an ID
- **THEN** system imports `nanoid` from the `nanoid` package

#### Scenario: Generate ID using nanoid

- **WHEN** the application creates a new todo
- **THEN** system calls `nanoid()` to generate the ID

### Requirement: Backward compatibility

The system SHALL continue to accept and work with existing UUID-format IDs in storage.

#### Scenario: Read existing UUID-format IDs

- **WHEN** the application loads todos from storage
- **THEN** system can still read and process todos with UUID-format IDs

#### Scenario: Generate new format for new todos

- **WHEN** the application creates a new todo
- **THEN** system generates a nanoid-format ID (not UUID)
