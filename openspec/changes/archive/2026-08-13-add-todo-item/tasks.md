# Tasks: Add Todo Item Management

## 1. Project Setup

- [x] Create `pyproject.toml` with project metadata (name: snekdo, Python >=3.11)
- [x] Create package directory `snekdo/` with `__init__.py`
- [x] Create `tests/` directory with `__init__.py`
- [x] Add `.gitignore` entries for `snekdo.egg-info`, `*.egg-info`, `.pytest_cache`

## 2. Core — Models

- [x] Create `snekdo/models.py` with `Todo` dataclass (id, title, description, due, completed, created_at)
- [x] Add `TodoFilter` enum or TypedDict for list query parameters
- [x] Write unit tests in `tests/test_models.py`

## 3. Core — Storage

- [x] Create `snekdo/storage.py` with `TodoStorage` class
- [x] Implement `load()` — read JSON file, return list of `Todo`
- [x] Implement `save(todos)` — write list of `Todo` to JSON file
- [x] Implement `add(todo)` — append and persist
- [x] Implement `get(todo_id)` — find by ID
- [x] Implement `delete(todo_id)` — remove by ID
- [x] Add file locking with `fcntl.flock` for write operations
- [x] Write unit tests in `tests/test_storage.py`

## 4. CLI Layer

- [x] Create `snekdo/__main__.py` with `argparse` setup
- [x] Implement `add` subcommand: `--title`, `--description`, `--due`
- [x] Implement `list` subcommand: `--status`, `--limit`
- [x] Implement `complete` subcommand: positional `TODONUM`
- [x] Implement `delete` subcommand: positional `TODONUM`
- [x] Add error handling with user-friendly messages and non-zero exit codes
- [x] Write unit tests in `tests/test_cli.py`

## 5. Integration & Polish

- [x] Add a `README.md` with usage examples
- [x] Add a `tox.ini` or `pytest.ini` with test configuration
- [x] Run `pytest` and confirm all tests pass
- [x] Run `python -m snekdo --help` and verify output
