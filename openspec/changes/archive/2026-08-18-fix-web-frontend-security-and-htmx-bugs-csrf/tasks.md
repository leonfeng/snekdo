## 1. CSRF protection

- [x] 1.1 Add `get_csrf_token()` helper to generate and store CSRF token in session
- [x] 1.2 Add `verify_csrf_token()` helper to validate CSRF token from request
- [x] 1.3 Generate CSRF token on login and register, rotating on each login
- [x] 1.4 Include CSRF token in all web templates (add, edit, complete, delete, profile, password, account deletion)
- [x] 1.5 Add CSRF validation to all POST/PUT/DELETE web routes
- [x] 1.6 Invalidate CSRF token on logout