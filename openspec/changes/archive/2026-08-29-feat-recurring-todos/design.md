# Design: Recurring Todos

## Context

snekdo stores todos as a flat list in a single JSON file, accessed through
`TodoStorage` with `fcntl`/`fake_fcntl` file locking. The CLI (`snekdo/__main__.py`)
and the FastAPI app (`snekdo/api.py`) both share `TodoStorage` as the single
persistence boundary. The web layer renders Jinja2 templates in
`snekdo/templates/`.

Two callers today mark a todo completed: the CLI `complete` subcommand and
the API `POST /api/v1/todos/{id}/complete`. Both funnel through
`TodoStorage.complete_todo`, which makes that method the natural single place
to implement recurrence.

## Decisions

### Recurrence trigger point

Recurrence fires inside `TodoStorage.complete_todo(id, user_id=None)` immediately
after the target todo is marked completed and saved. This guarantees the
behavior is identical for CLI, API, and any future caller, and keeps the
"completion implies recurrence" rule unenforceable by mistake at call sites.

`complete_todo` currently acquires the file lock, loads, mutates, and saves.
The new occurrence is created and saved within the same locked section, so the
read-modify-write is atomic and two concurrent completions cannot create
duplicate next-occurrences.

### Next-occurrence computation

`next_due_date(due: str | None, repeat: str, now: datetime) -> str` lives in
`snekdo/models.py` (next to the model it serves) and is a pure function:

- Base date: `due` if set, else the date portion of `now`.
- `daily`: base + 1 day.
- `weekly`: base + 7 days.
- `monthly`: advance to the same day-of-month in the next month; if that day
  does not exist (e.g. Jan 31 -> Feb), clamp to the last valid day of the
  target month.
- `yearly`: advance to the same month/day next year; Feb 29 clamps to Feb 28
  in non-leap years.
- Returns an ISO `YYYY-MM-DD` string. If the result is before today (only
  possible when `due` was a past date on a recurring todo), advance forward by
  intervals until it is >= today.

### Model changes

`Todo` gains two fields:

- `repeat: str = "none"` — one of `none|daily|weekly|monthly|yearly`.
- `last_completed_at: str | None = None` — ISO 8601 timestamp set when the
  todo is completed (used for recurrence base when `due` is absent).

`to_dict` / `from_dict` round-trip both, with `from_dict` defaulting missing
keys to `"none"` / `None` so pre-existing `todos.json` files keep working.

### Recurrence creation

In `complete_todo`, after marking the matched todo completed:

1. If `todo.repeat == "none"`: save and return (no behavior change).
2. Else: build a new `Todo` copying `title`, `description`, `priority`,
   `user_id`, `repeat`; set `completed=False`, `due=next_due_date(...)`,
   `last_completed_at=None`, `created_at=now`, and let `__post_init__` assign a
   fresh `id`. Append and save.

The `repeat` rule itself is never cleared, so recurrence is self-sustaining.

### CLI `add --repeat`

- New `--repeat` choice flag (`none|daily|weekly|monthly|yearly`, default
  `none`) on the `add` subcommand.
- `handle_add` passes it into `Todo(...)` and validates via `Priority`-style
  enum or a simple membership check.

### List display

`handle_list` renders a compact repeat tag for recurring todos, e.g.
`[weekly]`, in a fixed-width column after Priority. Non-recurring todos show a
blank in that column so alignment is preserved.

### API

- `TodoCreate` gains `repeat: str = "none"` validated against the allowed set.
- `TodoUpdate` gains `repeat: str | None = None` (optional; omit to leave
  unchanged, matching the existing due/priority pattern).
- `TodoResponse` gains `repeat` and `last_completed_at`.
- The complete endpoint already calls `complete_todo`, so recurrence is
  inherited automatically.

## Alternatives Considered

- **Lazy expansion at list time** (generate occurrences on read): rejected
  because it makes storage non-deterministic and complicates the
  single-source-of-truth invariant; explicit created rows are simpler to
  test and sync.
- **A scheduler/cron process**: rejected as out of scope; recurrence is
  triggered by completion, which matches user intent and needs no background
  worker.

## Risks / Open Questions

- `due` validation currently rejects past dates on create; recurring
  occurrence creation must bypass strict "must be future" validation when the
  computed next date legitimately lands in the past relative to a delayed
  completion. Mitigation: `next_due_date` advances forward until >= today, so
  the stored `due` is always non-past.
- Sync (`push`) must preserve the new fields; the api_client serializes whole
  todo dicts, so this is expected to be transparent but is covered by an e2e
  sync check in tasks.
