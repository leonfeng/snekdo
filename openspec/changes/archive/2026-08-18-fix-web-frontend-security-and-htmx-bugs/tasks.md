## 1. CSRF protection

- [ ] 1.1 Add `get_csrf_token()` helper to generate and store CSRF token in session
- [ ] 1.2 Add `verify_csrf_token()` helper to validate CSRF token from request
- [ ] 1.3 Generate CSRF token on login and register, rotating on each login
- [ ] 1.4 Include CSRF token in all web templates (add, edit, complete, delete, profile, password, account deletion)
- [ ] 1.5 Add CSRF validation to all POST/PUT/DELETE web routes
- [ ] 1.6 Invalidate CSRF token on logout

## 2. HTMX rendering fixes

- [ ] 2.1 Fix delete todo to target `<tbody>` instead of `<tr>` for empty state
- [ ] 2.2 Fix profile form HTMX target to use an inner container
- [ ] 2.3 Fix complete todo to load fresh instance before saving
- [ ] 2.4 Fix delete account to handle HTMX requests (return HTML, not 302)

## 3. Form validation fixes

- [ ] 3.1 Replace FastAPI Form constraints in login with manual validation
- [ ] 3.2 Catch Pydantic v2 ValidationError in add_todo and edit_todo
- [ ] 3.3 Add allowed-values validation for priority field (high/medium/low)
- [ ] 3.4 Fix empty-string due-date handling in edit_todo

## 4. Logout fix

- [ ] 4.1 Change logout route from GET to POST
- [ ] 4.2 Update templates to use POST form for logout

## 5. E2E tests

- [ ] 5.1 Add e2e test for CSRF token in forms
- [ ] 5.2 Add e2e test for deleting last todo
- [ ] 5.3 Add e2e test for invalid priority on add
- [ ] 5.4 Add e2e test for empty login credentials
- [ ] 5.5 Add e2e test for POST logout
- [ ] 5.6 Add e2e test for delete account via HTMX

## 6. Verification

- [ ] 6.1 Run pytest to verify all tests pass
- [ ] 6.2 Run e2e tests to verify web frontend behavior
