## Context

Tech stack: Python 3.11+, standard library only, pytest with Playwright for E2E tests.
Package layout: snekdo/ (library) + tests/. Persist todos to ~/.snekdo/todos.json.
Prefer editing existing files over rewriting them in full.
pytest.ini must use INI `[pytest]` keys, not pyproject `[tool.pytest.ini_options]`.

The `_row()` helper in `tests/e2e/test_todos.py` returns a coroutine instead of a Playwright Locator because `.first` is not awaited. This causes `AttributeError: 'coroutine' object has no attribute 'locator'` in 7 test functions.

## Goals / Non-Goals

**Goals:**
- Fix `_row()` to properly await `.first`, returning a resolved Locator
- Enable 7 E2E tests to pass: test_edit_todo, test_edit_todo_empty_title, test_complete_todo, test_complete_todo_redirect, test_delete_todo, test_delete_todo_redirect, test_show_todo

**Non-Goals:**
- No API or implementation changes needed - pure test helper fix
- No changes to the Todo model or storage logic

## Decisions

- Await `.first` in `_row()` to return a resolved Playwright Locator instead of a coroutine
- This is a minimal, targeted fix affecting only the test helper function

## Risks / Trade-offs

- [Risk] Minimal - single line change with `await`
- [Mitigation] No regression risk; the fix directly addresses the documented issue

## Open Questions

None