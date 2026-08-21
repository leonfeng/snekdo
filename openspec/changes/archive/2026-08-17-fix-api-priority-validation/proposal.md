## Why

`TodoCreate` and `TodoUpdate` in `snekdo/api.py` declare `priority` as a plain
`str` field with no enum constraint. This means the API accepts invalid priority
values like `"urgent"` or `"critical"` and stores them, breaking the priority
sorting logic and violating the `todo-priority` capability.

## What Changes

- Add `enum=["low", "medium", "high"]` to the `TodoCreate.priority` field.
- Add `enum=["low", "medium", "high"]` to the `TodoUpdate.priority` field.
- Add API-level scenarios to the `todo-priority` OpenSpec capability.

## Capabilities

### Modified Capabilities

- `todo-priority`: Add an API-level requirement "Validate priority values via API"
  with scenarios for invalid and empty priority values on `POST` and `PUT`.

## Impact

- **Affected code**: `snekdo/api.py` (`TodoCreate`, `TodoUpdate`).
- **No new dependencies**.
- **Compatibility**: Invalid priority values that were previously accepted will
  now return `422` validation errors.
