## 1. Implementation

- [x] 1.1 Update `snekdo/web_auth.py` `register_submit` to set `created_at=datetime.now().isoformat()` when creating the `User`.
- [x] 1.2 Add a test in `tests/test_web.py` verifying that a web-registered user has a non-empty `created_at`.

## 2. Verification

- [x] 2.1 Run the relevant tests to confirm the fix works.
- [x] 2.2 Run `openspec validate` to confirm the change is valid.
