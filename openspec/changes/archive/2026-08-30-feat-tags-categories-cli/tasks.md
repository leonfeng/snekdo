## 1. CLI: add command

- [x] 1.1 Add `--tag` (repeatable, `action="append"`) and `--category` flags to the `add` subparser in `snekdo/__main__.py`; pass both into `Todo` in `handle_add`

## 2. CLI: modify command

- [x] 2.1 Add `--tag` (repeatable) and `--category` flags to the `modify` subparser
- [x] 2.2 In `handle_modify`, pass `tags` to `storage.modify()` when any `--tag` is given (full replacement); pass `category` when `--category` is given (empty string clears)

## 3. CLI: list command

- [x] 3.1 Add `--tag` and `--category` filter flags to the `list` subparser
- [x] 3.2 In `handle_list`, apply tag filter (todo.tags contains tag) and category filter (exact match) before sorting/limiting, alongside existing status/priority filters

## 4. CLI: list output

- [x] 4.1 Add `Tags` column (comma-joined, cap 30, `...` truncation) and `Category` column (cap 20) after `Created At` in `handle_list` output, keeping single-space separators and header alignment

## 5. Tests

- [x] 5.1 CLI tests: `add` with one/multiple `--tag` and `--category`; defaults when omitted
- [x] 5.2 CLI tests: `modify` with `--tag` replaces tags, `--category` sets/clears, combinations leave unspecified fields unchanged
- [x] 5.3 CLI tests: `list --tag` and `--category` filters, combined with `--status`/`--priority`; "No todos found." when nothing matches
- [x] 5.4 CLI tests: new `Tags`/`Category` columns render correctly (comma-joined, empty, truncated) and header alignment is preserved
