# snekdo

A simple CLI todo list manager for Python.

## Features

- Add, list, complete, and delete todo items
- Persistent storage in JSON format
- Simple command-line interface
- File locking for concurrent access

## Installation

```bash
pip install -e .
```

## Usage

### Add a todo

```bash
snekdo add --title "Buy groceries" --description "Milk, eggs, bread" --due "2024-12-31"
```

### List todos

```bash
# List all todos
snekdo list --status all

# List pending todos
snekdo list --status pending

# List completed todos
snekdo list --status completed

# Limit results
snekdo list --limit 10
```

### Complete a todo

```bash
snekdo complete <todo-id>
```

### Delete a todo

```bash
snekdo delete <todo-id>
```

## Storage

Todos are stored in `~/.snekdo/todos.json` by default.

## Development

### Running tests

```bash
pytest
```

### Running with Python

```bash
python -m snekdo --help
```
