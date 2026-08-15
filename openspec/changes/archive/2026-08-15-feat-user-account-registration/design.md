## Context

The snekdo application is currently a single-user CLI todo manager with a FastAPI REST API and a Jinja2/HTMX web frontend. All todo data is stored in a single JSON file with no user isolation. The existing `Todo` model and `TodoStorage` class handle persistence, and the `snekdo/__main__.py` module implements CLI subcommands while `snekdo/api.py` implements the REST API.

## Goals / Non-Goals

**Goals:**
- Add user registration and login with JWT-based authentication.
- Enforce per-user todo isolation: each user can only access their own todos.
- Add CLI `register` and `login` subcommands for terminal-based account management.
- Add registration/login web pages to the Jinja2 frontend.
- Update the sync client to send authentication tokens.

**Non-Goals:**
- No OAuth or social login providers.
- No password reset or email verification.
- No role-based access control (all users are equal).
- No changes to the core `Todo` dataclass semantics beyond adding `user_id`.
- No database migration; JSON file storage is retained.

## Decisions

### Decision: Separate user storage file
- **Rationale**: Keep the todo storage focused on todos. Users are stored in a separate JSON file (`~/.snekdo/users.json`) using the same `TodoStorage` locking mechanism.
- **Alternative considered**: Embedding users in the same file. This couples user and todo data unnecessarily.
- **Implementation**: A new `UserStorage` class in `snekdo/storage.py` (or a separate `snekdo/user_storage.py`) mirrors `TodoStorage` with the same file locking pattern.

### Decision: Password hashing with passlib + bcrypt
- **Rationale**: passlib provides a clean API for password hashing/verification with bcrypt, which is widely supported and secure. The project already uses optional dependencies (fastapi, uvicorn), so adding `passlib` and `bcrypt` is consistent.
- **Alternative considered**: Using `itsdangerous` for password hashing. itsdangerous is better suited for token signing, not password hashing.
- **Implementation**: Use `passlib.context` with the `bcrypt` context for hashing and verification.

### Decision: JWT tokens with python-jose
- **Rationale**: python-jose is a well-known JWT library for Python. It supports both symmetric and asymmetric algorithms; we use HS256 with a secret key.
- **Alternative considered**: Using `itsdangerous` (already commonly used with Flask). However, python-jose is more standard for JWT in FastAPI.
- **Implementation**: Generate JWT with `sub` (user ID), `exp` (expiration), and `iat` (issued at). Store the secret key in an environment variable or config.

### Decision: JWT in Authorization header
- **Rationale**: The `Authorization: Bearer <token>` header is the standard way to send JWT tokens. FastAPI's `HTTPBearer` or `Depends` with a custom function can extract and validate it.
- **Alternative considered**: Using query parameters or cookies. Query parameters are less secure; cookies require CSRF protection.
- **Implementation**: A FastAPI dependency `get_current_user` that extracts the token from the `Authorization` header, validates it, and returns the user.

### Decision: Per-user todo filtering at the storage level
- **Rationale**: Filtering at the storage level ensures all operations (including sync) are isolated by user. The `Todo` model gets an optional `user_id` field.
- **Alternative considered**: Filtering at the API level only. This would not protect the CLI sync path.
- **Implementation**: `TodoStorage.load(user_id=None)` accepts an optional `user_id` and filters results. `TodoStorage.add(todo)` sets `user_id` if not already set.

### Decision: Token stored in a file for CLI and sync
- **Rationale**: The CLI and sync client need to persist the token between invocations. A file-based store (`~/.snekdo/credentials.json`) is simple and consistent with the existing storage approach.
- **Alternative considered**: Environment variable. Less convenient for CLI users.
- **Implementation**: `~/.snekdo/credentials.json` contains `{"access_token": "...", "token_type": "bearer"}`. The CLI reads this for sync; the sync client reads it for HTTP requests.

### Decision: Web sessions via JWT token in form
- **Rationale**: The web frontend uses JWT tokens stored in `localStorage` (JavaScript) rather than server sessions, keeping the API stateless.
- **Alternative considered**: Using FastAPI sessions with server-side session storage. This adds complexity and state.
- **Implementation**: The web frontend stores the JWT in `localStorage` and sends it in the `Authorization` header for all API requests. Registration/login forms submit to the auth endpoints.

### Decision: Authentication dependency for todo endpoints
- **Rationale**: A single FastAPI dependency `get_current_user` protects all todo endpoints. It extracts the token, validates it, and returns the user.
- **Alternative considered**: Per-endpoint authentication. This is error-prone and redundant.
- **Implementation**: `get_current_user` is a `Depends` dependency on all todo endpoints. Health check and auth endpoints are excluded.

## Risks / Trade-offs

- **Risk**: Storing tokens in a file on disk is less secure than a browser's secure storage.
  - **Mitigation**: The token file is stored in `~/.snekdo/` with restrictive permissions. The token is only useful if the attacker also has file system access.
- **Risk**: JWT tokens are not revocable without a token blacklist.
  - **Mitigation**: Short token expiration (e.g., 1 hour) limits the window of misuse. A blacklist can be added later.
- **Risk**: Adding `user_id` to `Todo` changes the storage format for existing todos.
  - **Mitigation**: Existing todos without `user_id` are treated as belonging to a "default" user or are filtered out. A migration step can be added.
- **Risk**: Password hashing adds a new dependency (passlib + bcrypt).
  - **Mitigation**: Made optional; only needed for the auth feature.
- **Risk**: Concurrent registration of the same username.
  - **Mitigation**: The user storage uses file locking; uniqueness is checked at write time.

## Migration Plan

- Existing todos without `user_id` will be loaded with `user_id=""` and treated as belonging to no user. The CLI `list` command (which doesn't require auth) will continue to work as before.
- Existing API users must update their clients to send the `Authorization` header.
- No data migration is required for the JSON storage format; the `user_id` field is optional on the `Todo` dataclass.

## Open Questions

- Should the token expiration be configurable? Default to 1 hour.
- Should there be a `snekdo logout` command to remove the stored token? Yes, this is trivial to add.
- Should the `Todo` model require `user_id` or keep it optional? Keep optional for backward compatibility with existing todos.
