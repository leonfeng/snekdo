## MODIFIED Requirements

### Requirement: Completing a recurring todo creates the next pending occurrence

The system SHALL, when a todo with `repeat != "none"` is marked completed, immediately create a new pending todo that:

- has a fresh unique `id`
- copies `title`, `description`, `priority`, `user_id`, and `repeat` from the source
- sets `completed = false`
- sets `due` to the computed next due date (per the requirement above)
- sets `last_completed_at` to `None`
- sets `created_at` to the current timestamp

The source todo SHALL be marked `completed = true` with its `last_completed_at` set to the current timestamp.

#### Scenario: Completing a weekly recurring todo creates the next occurrence

- **WHEN** a todo with `title = "Water plants"`, `repeat = weekly`, `due = 2026-08-29`, `user_id = "u1"` is completed at `2026-08-29T12:00:00`
- **THEN** the original todo has `completed = true` and `last_completed_at = "2026-08-29T12:00:00"`
- **AND** a new todo exists with `title = "Water plants"`, `repeat = weekly`, `due = "2026-09-05"`, `completed = false`, `user_id = "u1"`, and a new unique `id`

#### Scenario: Completing a non-recurring todo does not create a new todo

- **WHEN** a todo with `repeat = "none"` is completed
- **THEN** no new todo is created and the total todo count is unchanged

#### Scenario: Recurrence preserves priority and description

- **WHEN** a todo with `title = "Report"`, `description = "Weekly"`, `priority = "high"`, `repeat = weekly` is completed
- **THEN** the new occurrence has `title = "Report"`, `description = "Weekly"`, and `priority = "high"`

#### Scenario: Recurrence is idempotent to repeated completions of the same occurrence

- **WHEN** a user completes the same recurring occurrence twice (e.g., via CLI and API)
- **THEN** only one new pending occurrence is created (completion of an already-completed todo is a no-op for recurrence)

#### Scenario: Idempotency holds for an already-completed occurrence on any storage backend

- **WHEN** a recurring todo that is already `completed = true` is completed again on either the JSON or SQLite storage backend
- **THEN** no additional pending occurrence is created and the pending occurrence count is unchanged
