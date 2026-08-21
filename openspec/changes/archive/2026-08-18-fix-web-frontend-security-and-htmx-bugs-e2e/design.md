## Context

The web frontend security and HTMX bug fixes introduce new behavior that needs end-to-end testing. The e2e tests will verify the new behavior in a browser-like setting using Playwright.

## Goals / Non-Goals

**Goals:**
- Add e2e tests for CSRF token in forms, deleting last todo, invalid priority on add, empty login credentials, POST logout, and delete account via HTMX.
- Run pytest and e2e tests to verify all tests pass.

**Non-Goals:**
- No implementation changes (handled by other child changes).
- No changes to the test framework (pytest + Playwright).

## Decisions

- Use Playwright for e2e testing (consistent with existing e2e test infrastructure).
- E2e tests use the CSRF token from the session/cookies for form submissions.

## Migration Plan

1. Add e2e test for CSRF token in forms (task 5.1).
2. Add e2e test for deleting last todo (task 5.2).
3. Add e2e test for invalid priority on add (task 5.3).
4. Add e2e test for empty login credentials (task 5.4).
5. Add e2e test for POST logout (task 5.5).
6. Add e2e test for delete account via HTMX (task 5.6).
7. Run pytest to verify all tests pass (task 6.1).
8. Run e2e tests to verify web frontend behavior (task 6.2).