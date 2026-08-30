## 1. Model

- [x] 1.1 Add `tags: list[str]` (default `[]`) and `category: str | None` (default `None`) to the `Todo` dataclass in `snekdo/models.py`.
- [x] 1.2 Extend `Todo.to_dict()` to serialize `tags` and `category`.
- [x] 1.3 Extend `Todo.from_dict()` to load `tags` and `category` with backward-compatible defaults (`[]` and `None` when keys are missing or empty).

## 2. Tests

- [x] 2.1 Model tests: defaults, round-trip, and backward-compatible loading from old-format JSON (missing keys).
