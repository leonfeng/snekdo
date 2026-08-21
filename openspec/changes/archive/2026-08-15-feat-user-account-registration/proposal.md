## Why

The snekdo application currently has no user accounts — anyone with access to the storage file can read, modify, or delete all todos. Adding user account registration and authentication enables multi-user isolation so each user has their own private todo list, and allows the API and web UI to enforce per-user access control.

## What Changes

- Add a `User` model and user storage layer for registering and authenticating users (username + password hash).
- Add authentication endpoints: `POST /api/v1/auth/register` and `POST /api/v1/auth/login` that issue JWT tokens.
- Add per-user todo isolation: every `Todo` records a `user_id`; all list/show/create/update/delete endpoints require a valid token and operate only on the authenticated user's todos.
- Add a `snekdo register` CLI subcommand and `snekdo login` CLI subcommand so users can create accounts and obtain tokens from the terminal.
- Add a registration/login form to the Jinja2 web frontend (`/auth/register`, `/auth/login`).
- Update the sync command to send the authentication token with requests.
- Update the `Todo` dataclass to include an optional `user_id` field.

## Capabilities

### New Capabilities

- `user-auth`: User registration, login, and JWT-based authentication for the snekdo API and CLI.

### Modified Capabilities

- `fastapi-backend`: Todo endpoints now require authentication and filter by the requesting user's ID.
- `cli-sync`: Sync client sends the `Authorization` token header and handles 401/403 responses.
- `htmx-jinja2-frontend`: Adds registration/login pages and protects todo routes by redirecting to login when unauthenticated.

## Impact

- **New files**: `snekdo/models.py` (User model + user storage), `snekdo/auth.py` (JWT utilities, password hashing), `snekdo/api_auth.py` (auth endpoints + auth dependency), `snekdo/web_auth.py` (web auth routes), `tests/test_auth.py`.
- **Modified files**: `snekdo/models.py` (add `user_id` to `Todo`), `snekdo/storage.py` (per-user filtering), `snekdo/api.py` (auth-required todo endpoints), `snekdo/__main__.py` (register/login CLI subcommands), `snekdo/api_client.py` (token header), `snekdo/web.py` (auth web routes + login redirect).
- **New dependencies**: `python-jose` (JWT), `passlib` + `bcrypt` (password hashing), `itsdangerous` (optional, as alternative).
- **Breaking changes**: Existing API endpoints now require authentication; existing CLI sync requires a token. Unauthenticated access returns 401.
