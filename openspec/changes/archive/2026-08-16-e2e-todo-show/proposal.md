## Why

Viewing todo details is an important user action. E2E tests verify that users
can view the full details of a single todo and that non-existent todos return
a 404 response.

## What Changes

- Add E2E tests for showing todo details in `tests/e2e/test_todos.py`

## Capabilities

### New Capabilities

- `e2e-todo-show`: End-to-end tests for showing todo details.