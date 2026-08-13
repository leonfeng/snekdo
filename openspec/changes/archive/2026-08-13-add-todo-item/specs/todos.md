# Spec: Todos

## Purpose

Define the requirements for managing todo items in the snekdo application. Users must be able to create, list, complete, and delete todo items with optional descriptions and due dates, all persisted to a local JSON file.

## Requirements

### ADD `todo add` — Add a todo item

A user can add a new todo item with a title, and optionally a description and/or due date.

- **SHOULD** require a `--title` (or positional) argument for the todo title
- **SHOULD** accept an optional `--description` flag for additional details
- **SHOULD** accept an optional `--due` flag for a due date (e.g. `--due "2024-12-31"`)
- **MUST** generate a unique ID for each new todo item
- **MUST** set the `completed` status to `false` by default
- **MUST** persist the new item to the todos storage immediately

### REQ-002: LIST — List all todo items

A user can view all todo items, optionally filtered by completion status.

- **SHOULD** display all required fields: ID, title, description, due date, completed status
- **SHOULD** support a `--limit` flag to restrict the number of results
- **SHOULD** support a `--status` flag with values `all`, `pending`, `completed`
- **MUST** display items in reverse chronological order (newest first) by default

### REQ-003: COMPLETE — Mark a todo item as complete

A user can mark an existing todo item as completed by its ID.

- **MUST** accept the ID of the todo item as a required argument
- **MUST** update the `completed` field to `true`
- **MUST** persist the change immediately
- **MUST** report an error if the ID does not exist

### REQ-004: DELETE — Delete a todo item

A user can remove a todo item by its ID.

- **MUST** accept the ID of the todo item as a required argument
- **MUST** remove the item from storage
- **MUST** report an error if the ID does not exist
- **MUST** persist the deletion immediately

### REQ-005: ERROR HANDLING — Handle errors gracefully

- **MUST** report a clear error message when the storage file is missing or corrupted
- **MUST** report a clear error message when a requested resource does not exist
- **MUST** exit with a non-zero status code on error