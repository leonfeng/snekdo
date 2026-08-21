## 1. Add `--server` argument to CLI parsers

- [x] 1.1 Add `--server` argument to the `profile` subcommand parser in `create_parser()`.
- [x] 1.2 Add `--server` argument to the `profile-update` subcommand parser in `create_parser()`.
- [x] 1.3 Add `--server` argument to the `change-password` subcommand parser in `create_parser()`.
- [x] 1.4 Add `--server` argument to the `delete-account` subcommand parser in `create_parser()`.

## 2. Update CLI handlers to use `args.server`

- [x] 2.1 Update `handle_profile()` to use `args.server` instead of the hardcoded `http://127.0.0.1:8000`.
- [x] 2.2 Update `handle_profile_update()` to use `args.server` instead of the hardcoded `http://127.0.0.1:8000`.
- [x] 2.3 Update `handle_change_password()` to use `args.server` instead of the hardcoded `http://127.0.0.1:8000`.
- [x] 2.4 Update `handle_delete_account()` to use `args.server` instead of the hardcoded `http://127.0.0.1:8000`.

## 3. Update OpenSpec artifacts

- [x] 3.1 Create `specs/cli-server-url/spec.md` with the general server URL configuration capability.
- [x] 3.2 Update `specs/user-profile/spec.md` with CLI-level requirements for `profile`, `profile-update`, and `change-password`.
- [x] 3.3 Update `specs/user-account-deletion/spec.md` with CLI-level requirements for `delete-account`.

## 4. Verify

- [x] 4.1 Run `uv run pytest` to confirm existing tests still pass.
- [x] 4.2 Run `uv run snekdo profile --help` to confirm `--server` is recognized.
- [x] 4.3 Run `uv run snekdo delete-account --help` to confirm `--server` is recognized.