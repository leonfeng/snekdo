## 1. Sync client payloads

- [x] 1.1 Update `ServerHttpClient` in `snekdo/api_client.py` to include `tags` and `category` in create and update payloads

## 2. Tests

- [x] 2.1 Sync tests: create/update payloads include `tags` and `category`
- [x] 2.2 Sync test: push/pull round-trip preserves `tags` and `category` (including empty list / None)
