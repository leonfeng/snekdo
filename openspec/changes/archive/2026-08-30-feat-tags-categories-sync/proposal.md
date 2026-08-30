# Proposal: Tags & Categories — Sync

## Why

`snekdo sync` round-trips todos between local JSON and the server. Once todos carry `tags` and `category`, the sync client must carry those fields too, or they are silently dropped on push.

## What Changes

- `ServerHttpClient` create/update payloads include `tags` and `category`.
- Sync pull/push/both preserve the new fields without loss.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `cli-sync`: sync payloads carry `tags` and `category` so they round-trip between local and server.

## Impact

- `snekdo/api_client.py`: payload construction in create/update paths.
- Tests: sync client unit tests + an end-to-end push/pull round-trip that preserves the fields.
