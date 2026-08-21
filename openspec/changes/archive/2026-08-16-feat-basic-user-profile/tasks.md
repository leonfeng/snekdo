## 1. Update User model

- [x] 1.1 Add `display_name` and `email` fields to the `User` dataclass in `snekdo/models.py`
- [x] 1.2 Update `User.to_dict()` to include `display_name` and `email`
- [x] 1.3 Update `User.from_dict()` to deserialize `display_name` and `email`

## 2. Update UserStorage

- [x] 2.1 Add `update_profile(user_id, display_name, email)` method to `UserStorage` in `snekdo/storage.py`
- [x] 2.2 Add `update_password(user_id, current_password, new_password)` method to `UserStorage`
- [x] 2.3 Add `get_profile(user_id)` helper that returns a User without password_hash

## 3. Update API Pydantic models

- [x] 3.1 Add `UserUpdate` model with optional `display_name` and `email` fields in `snekdo/api.py`
- [x] 3.2 Add `PasswordChange` model with `current_password`, `new_password`, `confirm_password` in `snekdo/api.py`
- [x] 3.3 Add `UserProfileResponse` model with `id`, `username`, `display_name`, `email`, `created_at` in `snekdo/api.py`
- [x] 3.4 Update `UserResponse` in `snekdo/api_auth.py` to include `display_name` and `email`

## 4. Add API endpoints

- [x] 4.1 Add `GET /api/v1/users/me` endpoint to view the current user's profile
- [x] 4.2 Add `PUT /api/v1/users/me` endpoint to update the current user's profile
- [x] 4.3 Add `PUT /api/v1/users/me/password` endpoint to change the current user's password
- [x] 4.4 Ensure all profile endpoints require authentication via `get_current_user`

## 5. Update API client

- [x] 5.1 Add `get_profile()` method to `ServerHttpClient` in `snekdo/api_client.py`
- [x] 5.2 Add `update_profile()` method to `ServerHttpClient`
- [x] 5.3 Add `change_password()` method to `ServerHttpClient`

## 6. Add CLI commands

- [x] 6.1 Add `profile` subcommand to view the current user's profile
- [x] 6.2 Add `profile update` subcommand to update display name and/or email
- [x] 6.3 Add `change-password` subcommand to change the user's password

## 7. Add tests

- [x] 7.1 Add tests for the new User model fields
- [x] 7.2 Add tests for UserStorage update methods
- [x] 7.3 Add tests for the new API endpoints
- [x] 7.4 Add tests for the new CLI commands

## 8. Update existing tests

- [x] 8.1 Update existing auth tests to account for new User fields
- [x] 8.2 Update existing storage tests if needed