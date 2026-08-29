## Purpose

Defines how a todo can carry a repeat rule and how completing a recurring todo automatically produces the next pending occurrence with a correctly computed due date.

## ADDED Requirements

### Requirement: Repeat rule is stored on the Todo model

The system SHALL store a `repeat` field on each todo with a value from the set `{"none", "daily", "weekly", "monthly", "yearly"}` and default it to `"none"` for todos that do not repeat.

#### Scenario: New todo without repeat flag defaults to none

- **WHEN** a user adds a todo without specifying a repeat interval
- **THEN** the stored todo has `repeat == "none"`

#### Scenario: New todo with repeat flag stores the chosen interval

- **WHEN** a user adds a todo with `--repeat weekly`
- **THEN** the stored todo has `repeat == "weekly"`

#### Scenario: Deserializing a stored todo without a repeat key defaults to none

- **WHEN** a JSON todo object without a `repeat` key is loaded
- **THEN** the resulting `Todo` has `repeat == "none"`

### Requirement: Next due date is computed from the repeat rule

The system SHALL compute the next due date for a completed recurring todo based on its `due` (or completion date when `due` is absent) and its `repeat` rule:

- `daily`: next calendar day
- `weekly`: same weekday one week later (7 days)
- `monthly`: same day of the next month, clamped to the last day of the month when the day does not exist
- `yearly`: same month/day one year later; February 29 clamps to February 28 in non-leap years

The computed date SHALL be in `YYYY-MM-DD` format and SHALL be on or after today's date.

#### Scenario: Daily recurrence advances by one day

- **WHEN** a completed todo with `due = 2026-08-29` and `repeat = daily` is completed
- **THEN** the new occurrence has `due = 2026-08-30`

#### Scenario: Weekly recurrence advances by seven days

- **WHEN** a completed todo with `due = 2026-08-29` and `repeat = weekly` is completed
- **THEN** the new occurrence has `due = 2026-09-05`

#### Scenario: Monthly recurrence on a normal day

- **WHEN** a completed todo with `due = 2026-08-15` and `repeat = monthly` is completed on or after 2026-08-15
- **THEN** the new occurrence has `due = 2026-09-15`

#### Scenario: Monthly recurrence clamps to end of month

- **WHEN** a completed todo with `due = 2026-01-31` and `repeat = monthly` is completed on or after 2026-01-31
- **THEN** the new occurrence has `due = 2026-02-28`

#### Scenario: Yearly recurrence on a normal day

- **WHEN** a completed todo with `due = 2026-05-10` and `repeat = yearly` is completed on or after 2026-05-10
- **THEN** the new occurrence has `due = 2027-05-10`

#### Scenario: Yearly recurrence on Feb 29 clamps to Feb 28 in a non-leap year

- **WHEN** a completed todo with `due = 2024-02-29` and `repeat = yearly` is completed on or after 2024-02-29
- **THEN** the new occurrence has `due = 2025-02-28`

#### Scenario: Completed todo without a due date uses the completion date

- **WHEN** a completed recurring todo has `due = None` and `last_completed_at = 2026-08-29T12:00:00` and `repeat = daily`
- **THEN** the new occurrence has `due = 2026-08-30`

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
