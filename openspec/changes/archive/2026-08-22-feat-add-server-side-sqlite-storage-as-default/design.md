## Context

The snekdo application currently uses JSON file-based storage via `TodoStorage` in `snekdo/storage.py`. All todo data is persisted to `~/.snekdo/todos.json`. This design introduces SQLite as an alternative storage backend.

## Goals / Non-Goals

**Goals:**
- Provide SQLite-backed storage as the default option
- Maintain backward compatibility with JSON storage during transition
- Improve performance and concurrency for users with large todo lists

**Non-Goals:**
- Remove JSON storage support entirely (keep as fallback)
- Change the API endpoint structure
- Modify the Todo model fields

## Decisions

- Use SQLAlchemy Core (lightweight ORM) for SQLite interaction to keep dependencies minimal
- Store the database path in the same location as the current JSON file (`~/.snekdo/todos.json`) but with `.db` extension
- Maintain the same `Todo` model interface; SQLite backend converts to/from dict format internally

## Risks / Trade-offs

- [SQLite concurrency] Multiple processes writing simultaneously could cause locking issues - mitigate with WAL mode and proper connection handling
- [Migration path] Existing JSON users need a migration script - will include opt-in migration tool
- [Dependency] Adding SQLAlchemy increases package size - using only core features to minimize impact

## Open Questions

- Should the default storage path automatically migrate from JSON to SQLite, or require explicit user opt-in?
- What SQLite dialect/features are safe to use across platforms (Linux, macOS, Windows)?
