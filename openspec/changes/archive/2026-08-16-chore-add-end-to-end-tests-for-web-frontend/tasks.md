## 1. Setup

- [x] 1.1 Add `playwright` to `pyproject.toml` `[project.optional-dependencies]` → `dev`
- [x] 1.2 Create `tests/e2e/` directory with `__init__.py` and `conftest.py`

## 2. E2E test fixture

- [x] 2.1 Create `tests/e2e/conftest.py` with a fixture that builds the FastAPI app,
  registers web routes, and provides a Playwright page
- [x] 2.2 Add a `pytest.ini` marker registration for `e2e` (optional, so unit tests
  are not slowed down)

## 3. Auth E2E tests (delegated to sub-changes)

- [x] 3.1 `e2e-auth-registration`: registration flow (valid + invalid)
- [x] 3.2 `e2e-auth-login`: login flow (valid + invalid)
- [x] 3.3 `e2e-auth-logout`: logout flow

## 4. Todo E2E tests (delegated to sub-changes)

- [x] 4.1 `e2e-todo-list`: empty list placeholder + list rows
- [x] 4.2 `e2e-todo-add`: add todo (valid + empty title error)
- [x] 4.3 `e2e-todo-edit`: edit todo (pre-fill, valid update, empty title error)
- [x] 4.4 `e2e-todo-complete`: complete todo (HTMX + redirect)
- [x] 4.5 `e2e-todo-delete`: delete todo (HTMX + redirect)
- [x] 4.6 `e2e-todo-show`: show todo details (valid + 404)

## 5. Profile E2E tests (delegated to sub-changes)

- [x] 5.1 `e2e-profile-view`: profile page renders with user info
- [x] 5.2 `e2e-profile-update`: update display name + email (valid + invalid format)
- [x] 5.3 `e2e-profile-password`: change password (valid + wrong current + short + mismatch)

## 6. Verification

- [x] 6.1 Run `pytest tests/e2e/ -m e2e` to verify all E2E tests pass across all sub-changes
- [x] 6.2 Run the full unit test suite to ensure no regressions

## Sub-changes

The following sub-changes were created to decompose this change:

- `e2e-auth-registration` — registration E2E tests
- `e2e-auth-login` — login E2E tests
- `e2e-auth-logout` — logout E2E tests
- `e2e-todo-list` — todo list page E2E tests
- `e2e-todo-add` — add todo E2E tests
- `e2e-todo-edit` — edit todo E2E tests
- `e2e-todo-complete` — complete todo E2E tests
- `e2e-todo-delete` — delete todo E2E tests
- `e2e-todo-show` — show todo details E2E tests
- `e2e-profile-view` — profile view E2E tests
- `e2e-profile-update` — profile update (name/email) E2E tests
- `e2e-profile-password` — password change E2E tests