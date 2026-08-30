# Proposal: Tags & Categories — REST API

## Why

The CLI is now able to set and filter tags/categories, but the REST API (used by sync, clients, and the web backend) still ignores them. This slice adds `tags` and `category` to the API request/response models and adds `tag`/`category` query filters on the list endpoint.

## What Changes

- `TodoCreate` and `TodoUpdate` gain `tags: list[str] = []` and `category: str | None = None`.
- `TodoResponse` (and `from_todo`) includes both fields.
- `POST /api/v1/todos` and `PUT /api/v1/todos/{id}` accept and persist the fields; on PUT, `tags` replaces the list and `category=None` clears it.
- `GET /api/v1/todos` gains optional `tag` and `category` query parameters.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `fastapi-backend`: request/response models include `tags`/`category`; list endpoint supports `tag` and `category` query filters.

## Impact

- `snekdo/api.py`: Pydantic models, create/update/list handlers, response mapping.
- Tests: API tests for create/modify with tags+category, list filters, and response inclusion.
