# Proposal: Tags & Categories — Model

## Why

Users need a way to organize todos beyond priority and due date. This change adds `tags` (list of strings) and `category` (optional string) fields to the `Todo` model with backward-compatible serialization. It is the foundation for all downstream slices (storage, CLI, API, sync, web).

## What Changes

- `Todo` dataclass gains `tags: list[str]` (default `[]`) and `category: str | None` (default `None`).
- `to_dict()` serializes both new fields.
- `from_dict()` loads them with backward-compatible defaults: missing `tags` key → `[]`, missing `category` key → `None`.

## Capabilities

### New Capabilities

- `todo-tags`: model-level storage and serialization of `tags` and `category` fields on `Todo`.

### Modified Capabilities

(none — this slice only adds new model fields; it does not change existing behavior of other capabilities)

## Impact

- `snekdo/models.py`: `Todo` dataclass, `to_dict`, `from_dict`.
- Tests: `tests/test_models.py` — add tests for defaults, round-trip, and backward-compatible loading.
