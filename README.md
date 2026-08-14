# snekdo

A simple CLI todo list manager for Python.

## Features

- Add, list, show, complete, modify, and delete todo items
- Persistent storage in JSON format
- File locking for concurrent access
- Priority levels (low, medium, high) with filtering
- Sorting by created date, title, priority, or completion status, with reverse order support
- Custom storage path via `--storage` flag
- REST API backend via FastAPI with `snekdo serve`

## Installation

```bash
pip install -e .
```

To use the REST API backend, install with the `api` extra:

```bash
pip install -e ".[api]"
```

## Usage

### Add a todo

```bash
snekdo add --title "Buy groceries" --description "Milk, eggs, bread" --due "2024-12-31" --priority medium
```

### List todos

```bash
# List all todos (including completed)
snekdo list --status all

# List pending todos (default)
snekdo list

# List completed todos
snekdo list --status completed

# Limit results
snekdo list --limit 10

# Filter by priority
snekdo list --priority high

# Sort by title (ascending)
snekdo list --sort title

# Sort by priority (descending)
snekdo list --sort priority --reverse

# Sort by creation date (ascending)
snekdo list --sort created_at
```

### Complete a todo

```bash
snekdo complete <todo-id>
```

### Delete a todo

```bash
snekdo delete <todo-id>
```

### Modify a todo

```bash
snekdo modify <todo-id> --title "New title" --description "New description" --due "2024-12-31" --priority high
```

### Show a todo

```bash
snekdo show <todo-id>
```

This displays all details of the specified todo item, including ID, Title, Description, Due, Priority, Status, and Created At.

### Serve the REST API

Start the FastAPI server:

```bash
snekdo serve
```

This starts the server on `127.0.0.1:8000` by default. You can customize the host and port:

```bash
snekdo serve --host 0.0.0.0 --port 9000 --storage /path/to/todos.json
```

The API exposes the following endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/todos` | List all todos |
| GET | `/api/v1/todos/{id}` | Show a single todo |
| POST | `/api/v1/todos` | Add a new todo |
| POST | `/api/v1/todos/{id}/complete` | Mark a todo as complete |
| PUT | `/api/v1/todos/{id}` | Modify a todo |
| DELETE | `/api/v1/todos/{id}` | Delete a todo |

OpenAPI documentation is available at `/openapi.json` and a Swagger UI at `/docs`.

## Storage

Todos are stored in `~/.snekdo/todos.json` by default. You can use a custom path with the `--storage` flag:

```bash
snekdo list --storage /path/to/todos.json
```

## Development

### Running tests

```bash
pytest
```

### Running with Python

```bash
python -m snekdo --help
```
