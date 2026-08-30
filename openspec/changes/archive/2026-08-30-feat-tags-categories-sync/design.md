## Context

See proposal for motivation. `ServerHttpClient` in `snekdo/api_client.py` builds JSON payloads for create/update operations. The `Todo` model and API now support `tags`/`category` (delivered by model/storage/api slices).

## Goals / Non-Goals

**Goals:**
- `ServerHttpClient` includes `tags` and `category` in create/update payloads.
- Sync round-trip preserves both fields.

**Non-Goals:**
- No new sync directions or conflict-resolution logic.

## Decisions

1. **Include `tags` and `category` in payloads** built by `ServerHttpClient.create_todo` and `ServerHttpClient.update_todo`, reading from the `Todo` dataclass attributes.
2. **Always include both keys** in payloads (even when empty/None) so the server receives an explicit value and can apply "replace" / "clear" semantics consistently.

## Risks / Trade-offs

- [Payload size] → Negligible; tags/categories are small strings.
