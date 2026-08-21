## 1. Storage layer

- [x] 1.1 Add `delete_all_user_todos(user_id)` method to `TodoStorage` that removes all todos belonging to a user and persists the remaining todos.
- [x] 1.2 Add `delete_user(user_id)` method to `UserStorage` that removes a user by ID and persists the remaining users.

## 2. API endpoint (user-account-deletion-api)

- [x] 2.1 Add a `UserDeleteConfirm` Pydantic model with a `password` field to `snekdo/api.py`.
- [x] 2.2 Add `DELETE /api/v1/users/me` endpoint to `snekdo/api.py` that verifies the user's password, deletes all user todos, deletes the user, and returns a success message.
- [x] 2.3 Add validation for missing/empty password (422 response).

## 3. CLI command (user-account-deletion-cli)

- [x] 3.1 Add `delete-account` subcommand to `create_parser()` in `snekdo/__main__.py` with `--password` and `--storage` flags.
- [x] 3.2 Add `handle_delete_account()` function to `snekdo/__main__.py` that calls the API client and removes stored credentials on success.
- [x] 3.3 Wire the command into `handle_command()` dispatch.

## 4. API client (user-account-deletion-client)

- [x] 4.1 Add `delete_account(password, credentials_path)` method to `ServerHttpClient` in `snekdo/api_client.py`.

## 5. Web frontend (user-account-deletion-web)

- [x] 5.1 Add a delete account form/button to the profile page template.
- [x] 5.2 Add a `DELETE /profile` route (or `POST /profile/delete`) in `snekdo/web.py` that deletes the account and logs the user out.

## 6. E2E tests

- [x] 6.1 Create `openspec/specs/e2e-account-deletion/spec.md` with scenarios for account deletion via the web frontend.

## 7. Validation

- [x] 7.1 Run `openspec validate "feat-user-account-deletion"` to verify the change artifacts.
