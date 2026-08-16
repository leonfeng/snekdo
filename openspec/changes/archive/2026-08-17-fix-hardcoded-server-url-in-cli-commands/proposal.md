## Why

Several CLI commands (`profile`, `profile-update`, `change-password`, `delete-account`) hardcode the server base URL `http://127.0.0.1:8000` directly when constructing `ServerHttpClient`, while other server-facing commands (`sync`, `register`, `login`) already accept a `--server` flag. This means users cannot point these profile/account commands at a non-default server (e.g., a remote or locally-tuned server), creating an inconsistent and limiting experience.

## What Changes

- Add a `--server` argument (default `http://127.0.0.1:8000`) to the `profile`, `profile-update`, `change-password`, and `delete-account` CLI subcommands.
- Update the corresponding handlers to use `args.server` instead of the hardcoded URL.
- Introduce a general CLI server-URL capability and update affected spec capabilities to reflect the new requirements.

## Capabilities

### New Capabilities

- `cli-server-url`: Defines the general server URL configuration for all CLI commands that connect to a FastAPI server — every such command MUST accept `--server` and default to `http://127.0.0.1:8000`.

### Modified Capabilities

- `cli-sync`: The existing "Server URL configuration" requirement already covers `sync`; this change generalizes the pattern to all CLI commands.
- `user-profile`: Adds CLI-level requirements for `profile`, `profile-update`, and `change-password` to accept and use the `--server` flag.
- `user-account-deletion`: Adds a CLI-level requirement for `delete-account` to accept and use the `--server` flag.

## Impact

- **Affected code**: `snekdo/__main__.py` (argument parsers and handlers for `profile`, `profile-update`, `change-password`, `delete-account`).
- **No new dependencies**: The fix uses the existing `ServerHttpClient` and argparse infrastructure.
- **Compatibility**: Default behavior is unchanged — `--server` defaults to `http://127.0.0.1:8000` for all commands.