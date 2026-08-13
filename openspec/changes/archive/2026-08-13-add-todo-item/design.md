# Design: Todo Item Management

## Context

snekdo is a minimal Python CLI application for managing todo items. The application stores data in a local JSON file and exposes commands through the Unix shell. This change adds the core todo CRUD operations.

## Goals

- Provide a simple, fast CLI for todo management
- Persist todos to a local JSON file (`~/.snekdo/todos.json`)
- Support the four core operations: add, list, complete, delete
- Keep the dependency footprint minimal (standard library only)

## Architecture

```
snekdo/
├── snekdo/
│   ├── __main__.py      # CLI entry point (argparse)
│   ├── cli.py           # CLI command handlers
│   ├── models.py        # Todo model
│   └── storage.py       # JSON file I/O
├── tests/
│   ├── test_storage.py
│   └── test_cli.py
├── pyproject.toml
└── README.md
```

## Decisions

### D1: Use argparse for the CLI layer

The application uses Python's built-in `argparse` module to define subcommands (`add`, `list`, `complete`, `delete`). This avoids external dependencies and is the standard approach for Python CLIs.

### D2: Use a JSON file for persistence

Todo items are stored in a single JSON file (`~/.snekdo/todos.json`). This keeps the application simple and portable. A JSON file is sufficient for a single-user CLI tool and avoids the complexity of a database.

### D3: UUIDv7 for primary keys

Each todo item gets a `uuid7` identifier (or a UUIDv4 fallback) to ensure uniqueness without a sequence generator.

### D4: Flat list with in-memory filtering

The storage layer reads the full JSON array into memory on each operation and writes it back. This is acceptable for the expected scale (hundreds to low thousands of items).

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Concurrent writes corrupt the file | Low | High | Use `fcntl.flock` for file locking on write operations |
| Corrupted JSON file | Low | High | Catch `json.JSONDecodeError` and report a clear error |
| Large file size degrades performance | Low | Low | Accept as known limitation; add limit/pagination later |
| Missing storage directory | Low | Medium | Create `~/.snekdo/` on first write if it does not exist |

## Data Model

```python
@dataclass
class Todo:
    id: str
    title: str
    description: str
    due: str | None
    completed: bool
    created_at: str  # ISO 8601
```

## Error Model

- `TodoNotFoundError` — item with given ID does not exist
- `StorageError` — file read/write/parse failure
- All errors are surfaced to the user with a non-zero exit code