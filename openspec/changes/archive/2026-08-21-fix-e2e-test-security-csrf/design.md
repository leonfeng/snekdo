## Context

Tech stack: Python 3.11+, standard library only, pytest for tests. Package layout: snekdo/ (library) + tests/. Persist todos to ~/.snekdo/todos.json. Prefer editing existing files over rewriting them in full. pytest.ini must use INI `[pytest]` keys, not pyproject `[tool.pytest.ini_options]`.

Cross-cutting: E2E security tests in `tests/e2e/test_security.py`.

## Goals / Non-Goals

**Goals:**
- Fix CSRF token handling in form submissions to ensure mismatched tokens are properly rejected with 403
- Fix dynamic priority option creation in the add todo form to work with Playwright's DOM
- Fix CSRF token cookie invalidation on logout to properly clear the token

**Non-Goals:**
- No API changes needed - test infrastructure and frontend fixes only
- No changes to the core Todo model or storage logic

## Decisions

**CSRF token handling:** The form submissions need to include the CSRF token from the cookie. The test expects a 403 with "invalid csrf token" error when a mismatched token is submitted. The fix will involve ensuring the frontend reads the CSRF cookie and includes it in form submissions, and the backend validates it properly.

**Dynamic priority option creation:** The issue is with creating new priority options dynamically appended to the select element. The fix will involve ensuring the new option is properly created and selectable without causing Playwright evaluation errors.

**CSRF token invalidation on logout:** After logging out, the CSRF token cookie must be properly invalidated/cleared. The fix will involve ensuring the logout endpoint clears the CSRF cookie.

## Risks / Trade-offs

- [Risk] Frontend and backend CSRF coordination may be complex
  - [Mitigation] Follow existing patterns in the codebase for CSRF token handling

- [Risk] Dynamic option creation may have edge cases with DOM manipulation
  - [Mitigation] Test with various priority values and DOM states

- [Risk] Logout may not properly clear all cookie domains
  - [Mitigation] Ensure cookie path and domain are correctly set

## Open Questions

1. Should the CSRF token be read from a specific cookie name? (Check existing cookie names in the codebase)
2. How should the priority options be dynamically created - what mechanism is used?
3. What is the exact logout flow and how is the CSRF cookie currently handled?
