## Why

Completing a todo is a core user action. E2E tests verify that users can mark
todos as complete via both HTMX (AJAX) and traditional redirect, covering the
two interaction patterns supported by the web frontend.

## What Changes

- Add E2E tests for completing a todo in `tests/e2e/test_todos.py`

## Capabilities

### New Capabilities

- `e2e-todo-complete`: End-to-end tests for completing a todo.