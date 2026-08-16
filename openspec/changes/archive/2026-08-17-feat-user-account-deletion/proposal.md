## Why

Users need the ability to fully remove their account and all associated data from the snekdo platform. Currently, the API and CLI provide user registration, login, profile management, and password changes, but there is no way to delete an account. This leaves users with no way to exercise their right to be forgotten and creates orphaned user records.

## What Changes

- **New API endpoint**: `DELETE /api/v1/users/me` that allows an authenticated user to delete their own account, requiring password confirmation.
- **New CLI command**: `snekdo delete-account` that calls the API endpoint to delete the account and removes stored credentials.
- **New API client method**: `delete_account()` on `ServerHttpClient` for programmatic account deletion.
- **New web frontend**: A delete account button on the profile page with confirmation.
- **New storage methods**: `delete_user()` on `UserStorage` and `delete_all_user_todos()` on `TodoStorage` to support cascading deletion.
- **New e2e test**: Account deletion end-to-end test.

## Capabilities

### New Capabilities

- `user-account-deletion-api`: REST API endpoint `DELETE /api/v1/users/me`, storage methods (`delete_user`, `delete_all_user_todos`), cascading deletion of todos, and token invalidation after deletion.
- `user-account-deletion-cli`: CLI subcommand `snekdo delete-account` that authenticates the request using stored credentials and removes them on success.
- `user-account-deletion-client`: HTTP client method `delete_account()` on `ServerHttpClient` for programmatic account deletion.
- `user-account-deletion-web`: Web frontend delete account option on the profile page with confirmation and logout.

### Modified Capabilities

- `user-profile`: The profile page gains a delete account option (UI change only; the profile API itself is not changed).

## Impact

- **Affected code**: `snekdo/api.py` (new endpoint), `snekdo/storage.py` (new methods), `snekdo/__main__.py` (new CLI command), `snekdo/api_client.py` (new client method), `snekdo/web.py` (new web route), `snekdo/templates/profile.html` (new button).
- **New dependencies**: None. Uses existing `bcrypt` and `python-jose` for password verification and token handling.
- **Security**: Account deletion requires password confirmation. All user todos are deleted as part of the operation.
