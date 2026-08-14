# snekdo

A simple CLI todo list manager for Python.

## Features

- Add, list, show, complete, modify, and delete todo items
- Persistent storage in JSON format
- File locking for concurrent access
- Priority levels (low, medium, high) with filtering
- Sorting by created date, title, priority, or completion status, with reverse order support
- Custom storage path via `--storage` flag

## Installation

```bash
pip install -e .
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
