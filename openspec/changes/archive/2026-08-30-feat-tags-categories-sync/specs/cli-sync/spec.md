## MODIFIED Requirements

### Requirement: Sync client sends complete todo payloads

The sync client SHALL include `tags` (list of strings) and `category` (string or null) in the JSON payloads sent for creating and updating todos, so the fields round-trip between local storage and the server.

#### Scenario: Push new todo carries tags and category

- **WHEN** a local todo with `tags=["work"]` and `category="office"` is pushed to the server
- **THEN** the created remote todo has those same `tags` and `category` values

#### Scenario: Push modified todo carries updated tags and category

- **WHEN** a local todo's `tags` or `category` has changed and it is pushed
- **THEN** the remote todo reflects the updated values

#### Scenario: Pull preserves tags and category

- **WHEN** a remote todo has `tags` and `category` and is pulled to local storage
- **THEN** the local todo has those same values

#### Scenario: Todo without tags or category round-trips safely

- **WHEN** a todo with no tags and no category is pushed and pulled
- **THEN** the local copy ends up with `tags == []` and `category is None`
