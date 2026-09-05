## Context

See proposal.md - Why. The recurring-todos spec requires idempotent completion, but only the SQLite backend (`storage_sqlite.py:283`) guards against re-spawning on an already-completed todo. The JSON backend (`storage.py:183`) lacks that guard, so double-completing a recurring todo spawns duplicate occurrences. Both CLI (`__main__.py:565`) and API (`api.py:415`) delegate unconditionally to `storage.complete()`, so the fix must live in the storage layer.

## Goals / Non-Goals

**Goals:**
- Make the JSON `TodoStorage.complete()` path idempotent, matching SQLite behavior.
- Add regression tests proving double-completion creates only one occurrence on both backends.

**Non-Goals:**
- Changing the CLI/API surface or `next_due_date()` semantics.
- Fixing the timezone skew between the JSON (`datetime.now()`) and SQLite (`datetime.now(timezone.utc)`) backends — separate concern, out of scope.

## Decisions

- **Guard at the storage layer, not callers.** `handle_complete` and `complete_todo` both delegate without checking `completed`. Centralizing the guard in `TodoStorage.complete()` covers every entry point at once and keeps the invariant at the boundary where state is mutated. Alternative (checking in each caller) was rejected as it would need duplication across CLI, API, and web handlers.
- **Mirror SQLite's exact condition.** Use `if todo.repeat and todo.repeat != "none" and not todo.completed` in `storage.py` to keep the two backends behaviorally identical. SQLite is already correct, so it is the reference; JSON becomes a bug fix, not a redesign.
- **Add regression tests for both backends.** The bug is backend-specific, so tests must cover JSON and SQLite to prevent divergence from silently reappearing.

## Risks / Trade-offs

- [Behavioral change for stored data] → Existing duplicate occurrences (if any already exist from double-completion) are not cleaned up; this only stops new ones. Acceptable for a bug fix; no migration needed since the guard only prevents future duplicates.
- [Guard placement depends on `todo.completed` being freshly loaded] → Both backends load the todo row before deciding, so the guard sees the current persisted state; no staleness risk.
