## Why

Deleting a todo is a core user action. E2E tests verify that users can remove
todos via both HTMX (AJAX) and traditional redirect, covering the two
interaction patterns supported by the web frontend.

## What Changes

- Add E2E tests for deleting a todo in `tests/e2e/test_todos.py`

## Capabilities

### New Capabilities

- `e2e-todo-delete`: End-to-end tests for deleting a todo.