## Context

The snekdo project is a Python CLI todo list manager with a FastAPI REST API, Jinja2/HTMX web frontend, and sync capability. User accounts are managed via `snekdo/api_auth.py` (registration/login), `snekdo/storage.py` (UserStorage/TodoStorage), and `snekdo/web.py` (web routes). The user profile capability (`snekdo/api.py`) provides `GET/PUT /api/v1/users/me` and `PUT /api/v1/users/me/password`. There is no account deletion capability.

## Goals / Non-Goals

**Goals:**
- Add a `DELETE /api/v1/users/me` API endpoint with password confirmation.
- Cascade delete all todos belonging to the deleted user.
- Add a `snekdo delete-account` CLI command.
- Add a `delete_account()` method to `ServerHttpClient`.
- Add a delete account option to the web profile page.
- Add storage methods `delete_user()` and `delete_all_user_todos()`.

**Non-Goals:**
- Do not implement a token blacklist (JWT is stateless; deleted users are rejected because the user record no longer exists).
- Do not implement soft deletion (hard delete only).
- Do not implement account deletion via email confirmation.
- Do not modify the existing user registration, login, or profile update flows beyond adding the delete option.

## Decisions

### 1. Password confirmation for account deletion

**Decision**: Require the user's current password as confirmation in the request body.

**Rationale**: Account deletion is a destructive, irreversible action. Requiring the current password ensures that only the legitimate account owner (who knows the password) can delete the account. This is consistent with the existing `PUT /api/v1/users/me/password` flow which also requires `current_password`.

**Alternatives considered**:
- Use a confirmation token sent to email: More secure but adds complexity and a new dependency (SMTP).
- Use a separate "delete token" stored with the account: Adds storage complexity.
- No confirmation: Insecure; anyone with a valid token can delete the account.

### 2. Cascading deletion of todos

**Decision**: When a user deletes their account, all todos with `user_id` equal to the deleted user's ID are permanently deleted.

**Rationale**: Users should be able to fully remove their data. Keeping todos without an owner is not useful and violates the principle of data minimization.

**Alternatives considered**:
- Transfer todos to an admin: Adds complexity and is not appropriate for a personal todo app.
- Soft delete todos: Adds complexity and leaves orphaned data.
- Delete only the user record, not todos: Leaves orphaned data.

### 3. Storage method separation

**Decision**: Add `delete_user(user_id)` to `UserStorage` and `delete_all_user_todos(user_id)` to `TodoStorage`. The API endpoint calls both methods.

**Rationale**: This separates concerns — `UserStorage` manages user records, `TodoStorage` manages todos. The API layer orchestrates the cascade.

**Alternatives considered**:
- Single method on `UserStorage` that also deletes todos: Violates single responsibility; `UserStorage` shouldn't know about `TodoStorage`.
- Delete todos first, then user: Same result, but order doesn't matter much since both are required.

### 4. Token invalidation after deletion

**Decision**: Do not implement a token blacklist. After deletion, `get_current_user` already returns 401 because the user record no longer exists.

**Rationale**: JWT is stateless. The existing `get_current_user` dependency looks up the user by token's `sub` claim; if the user doesn't exist, it returns 401. This is sufficient for the spec's requirement that "a deleted user's JWT token cannot be used to authenticate."

**Alternatives considered**:
- Token blacklist: Requires a stateful store (Redis, DB). Adds complexity and a new dependency.
- Short-lived tokens: Reduces the window but doesn't solve the problem.

### 5. Web frontend confirmation

**Decision**: Use a JavaScript `confirm()` dialog for initial confirmation, then a modal or form for password entry.

**Rationale**: The existing web frontend uses HTMX and Jinja2. A simple `confirm()` dialog followed by a password form is consistent with the existing UI patterns.

**Alternatives considered**:
- No confirmation: Insecure.
- Email confirmation: Too complex for this feature.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Accidental account deletion | Require password confirmation and JavaScript `confirm()` dialog |
| Data loss | None — deletion is intentional and irreversible |
| Token still valid after deletion | `get_current_user` checks user existence, so deleted users are rejected |
| Race condition during deletion | Use file locking (existing `fcntl` mechanism) to ensure atomicity |
| Large user base (not applicable) | Not relevant for personal todo app |

## Migration Plan

No migration is needed. This is a new feature that does not affect existing data. The new storage methods are backward-compatible (they only add functionality).

## Open Questions

- **Should the web frontend use a modal dialog or a separate page for password confirmation?** A modal is more user-friendly but requires more template work. A separate page is simpler. Decision: Use a simple confirm() + form submission pattern consistent with existing web routes.
- **Should the CLI `delete-account` command accept `--password` as a flag or prompt interactively?** For scripting/automation, a flag is better. For security, interactive prompt is better. Decision: Accept `--password` flag for consistency with other CLI commands (e.g., `--storage`).
- **Should the API client `delete_account()` also clear the credentials file?** The CLI handler should handle credential removal; the client method should just make the API call. This separation keeps the client reusable.
