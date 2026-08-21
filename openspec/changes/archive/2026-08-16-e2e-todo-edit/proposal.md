## Why

Editing a todo is a core user action. E2E tests verify that users can update
existing todos from the web form and receive appropriate feedback for invalid
input.

## What Changes

- Add E2E tests for editing a todo in `tests/e2e/test_todos.py`

## Capabilities

### New Capabilities

- `e2e-todo-edit`: End-to-end tests for editing a todo.