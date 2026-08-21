## 1. Setup dependencies

- [x] 1.1 Add `passlib`, `bcrypt`, and `python-jose` to `pyproject.toml` as optional dependencies (or as regular dependencies).
- [x] 1.2 Create `snekdo/auth.py` module with JWT token generation/validation and password hashing utilities.

## 2. Add user model and storage

- [x] 2.1 Add a `User` dataclass to `snekdo/models.py` with `id`, `username`, `password_hash`, and `created_at` fields.
- [x] 2.2 Add a `UserStorage` class to `snekdo/storage.py` (or `snekdo/user_storage.py`) that persists users to `~/.snekdo/users.json` with the same file locking pattern as `TodoStorage`.
- [x] 2.3 Add an optional `user_id` field to the `Todo` dataclass in `snekdo/models.py`.
- [x] 2.4 Update `TodoStorage.load()` to accept an optional `user_id` and filter results by user.
- [x] 2.5 Update `TodoStorage.add()` to set `user_id` on a todo if not already set.
- [x] 2.6 Update `TodoStorage.get()` to filter by user_id when provided.

## 3. Implement authentication endpoints

- [x] 3.1 Create `snekdo/api_auth.py` with `POST /api/v1/auth/register` and `POST /api/v1/auth/login` endpoints.
- [x] 3.2 Define Pydantic request models `UserCreate` and `UserLogin` for registration and login.
- [x] 3.3 Define a `UserResponse` Pydantic model for the registered user (excluding password_hash).
- [x] 3.4 Implement a `get_current_user` FastAPI dependency that extracts and validates the JWT token from the `Authorization` header.
- [x] 3.5 Apply `get_current_user` to all todo CRUD endpoints in `snekdo/api.py`.
- [x] 3.6 Ensure `GET /api/v1/health` remains public (no auth required).
- [x] 3.7 Ensure auth endpoints (`/api/v1/auth/*`) remain public.

## 4. Add CLI register and login subcommands

- [x] 4.1 Add a `register` subparser to `create_parser()` in `snekdo/__main__.py` with `--username`, `--password`, and `--storage` arguments.
- [x] 4.2 Add a `login` subparser to `create_parser()` with `--username`, `--password`, and `--storage` arguments.
- [x] 4.3 Implement `handle_register()` to create a user account on the server and store the access token.
- [x] 4.4 Implement `handle_login()` to authenticate and store the access token in `~/.snekdo/credentials.json`.
- [x] 4.5 Add a `snekdo logout` subcommand to remove the stored credentials.

## 5. Update sync client for authentication

- [x] 5.1 Update `ServerHttpClient` to read the stored token from `~/.snekdo/credentials.json`.
- [x] 5.2 Update `ServerHttpClient._request()` to include the `Authorization: Bearer <token>` header when a token is available.
- [x] 5.3 Update `ServerHttpClient._request()` to treat `401` and `403` responses as authentication errors.
- [x] 5.4 Update the CLI sync command to report authentication errors gracefully.

## 6. Add web authentication routes

- [x] 6.1 Create `snekdo/web_auth.py` with `/auth/register`, `/auth/login`, and `/auth/logout` routes.
- [x] 6.2 Create Jinja2 templates `register.html` and `login.html` in `snekdo/templates/`.
- [x] 6.3 Protect todo routes by redirecting unauthenticated users to `/auth/login`.
- [x] 6.4 Add a logout button to the web UI.

## 7. Add tests

- [x] 7.1 Create `tests/test_auth.py` with tests for registration, login, and JWT validation.
- [x] 7.2 Add tests for per-user todo isolation.
- [x] 7.3 Add tests for the CLI register and login subcommands.
- [x] 7.4 Add tests for the sync client token header.

## 8. Update documentation

- [x] 8.1 Update `README.md` to describe the new register, login, and logout CLI commands.
- [x] 8.2 Update `README.md` to describe the authentication requirements for the API and sync.
