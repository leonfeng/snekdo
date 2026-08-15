## Why

The web registration form in `snekdo/web_auth.py` creates a `User` without setting `created_at`, leaving it as an empty string. The API registration endpoint correctly sets `created_at` to the current ISO 8601 timestamp, so web-registered users have an inconsistent (empty) `created_at` compared to API-registered users. This fix ensures all users have a valid `created_at` timestamp regardless of how they register.

## What Changes

- Update `snekdo/web_auth.py` `register_submit` to set `created_at=datetime.now().isoformat()` when creating a `User` from the web registration form.
- Add a test verifying that web-registered users have a non-empty `created_at`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `user-auth`: Web registration now records the `created_at` timestamp consistently with the API registration endpoint.

## Impact

- **Modified files**: `snekdo/web_auth.py`, `tests/test_web.py`
- **Behavior change**: Web-registered users will now have `created_at` set to the registration timestamp instead of an empty string.
- **No breaking changes** for existing users.
