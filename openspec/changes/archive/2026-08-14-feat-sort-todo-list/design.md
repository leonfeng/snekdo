## Context

The current implementation in `snekdo/__main__.py` has a hardcoded sort by `created_at` in descending order (newest first) at line 119. This is a simple sorting mechanism that doesn't allow users to control the sort order or choose different sort fields.

## Goals / Non-Goals

**Goals:**
- Add `--sort` flag to `list` command with choices: `created_at`, `title`, `priority`, `completed`
- Add `--reverse` flag to reverse the sort order
- Support sorting by date fields (created_at) in both ascending and descending order
- Support sorting by string fields (title) alphabetically
- Support sorting by enum fields (priority) with defined ordering
- Support sorting by boolean fields (completed) with consistent ordering
- Apply sorting after filtering but before limiting results
- Maintain backward compatibility (default behavior unchanged)

**Non-Goals:**
- No custom sort key functions
- No composite sort keys (e.g., sort by priority then by title)
- No database or complex storage-level sorting
- No caching of sorted results

## Decisions

### Decision: Use in-memory sorting with key functions

**Choice**: Implement sorting in the `handle_list` function using Python's built-in `sorted()` with custom key functions.

**Rationale**: 
- The todo list is expected to be small (hundreds to low thousands of items)
- In-memory sorting is simple to implement and test
- No additional dependencies required
- Consistent with the project's existing approach (e.g., `filter_by_priority` in storage)

**Alternatives considered**:
- Database-level sorting: Would require SQLite or similar, adding complexity
- Custom comparator: Python 3's `sorted()` with `key` is more idiomatic
- Lazy evaluation: Not necessary given expected data sizes

### Decision: Define explicit priority ordering

**Choice**: Map priority values to numeric sort keys: `high=3`, `medium=2`, `low=1`.

**Rationale**:
- Provides intuitive ordering (high priority first by default)
- Simple integer comparison is efficient
- Consistent with how priorities are displayed (high to low)

**Alternatives considered**:
- Alphabetical ordering: "high" < "low" < "medium" is not intuitive
- Custom enum: Would require more code but could be cleaner

### Decision: Handle None values consistently

**Choice**: For null/None values in sort fields, use a consistent approach:
- `created_at`: Empty string sorts last (newest first is default)
- `title`: Empty string sorts first
- `priority`: Missing priority treated as "medium" (default)
- `completed`: False (incomplete) sorts before True (completed)

**Rationale**:
- Consistent behavior is more predictable than undefined behavior
- Matches common UX patterns (empty values at the end for dates, at the beginning for strings)

**Alternatives considered**:
- Stable sort preserving original order: Could be confusing
- Error on null values: Too strict for optional fields

## Risks / Trade-offs

### Risk: Performance with large lists

**Impact**: Low - sorting is O(n log n) and lists are expected to be small.

**Mitigation**: If lists grow beyond ~10,000 items, consider pagination or database indexing.

### Risk: User confusion with sort order

**Impact**: Medium - users may not understand the difference between `--sort` and `--reverse`.

**Mitigation**: Clear error messages and help text explaining the flags.

### Risk: Backward compatibility

**Impact**: Low - default behavior remains unchanged.

**Mitigation**: Only change behavior when flags are explicitly provided.

## Migration Plan

This is a pure feature addition with no migration required. Existing behavior is preserved by default.

## Open Questions

None - all requirements are clearly defined.
