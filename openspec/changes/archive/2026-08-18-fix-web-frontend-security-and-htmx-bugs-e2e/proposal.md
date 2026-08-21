## Why

The web frontend security and HTMX bug fixes introduce new behavior that needs end-to-end testing: CSRF token presence in forms, deleting the last todo, invalid priority on add, empty login credentials, POST logout, and delete account via HTMX. Without e2e tests, these changes cannot be verified in a browser-like setting.

## What Changes

- Add e2e tests covering the new behavior (CSRF, last-todo delete, invalid priority, empty login, logout, delete account).
- Run pytest and e2e tests to verify all tests pass.

## Capabilities

No spec-level changes. This change is purely about adding tests and verification.

## Impact

- Affected code: `tests/e2e/`.
- No new dependencies.