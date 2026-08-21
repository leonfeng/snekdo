## Why

The HTMX/Jinja2 web frontend has several security and correctness bugs: invalid HTML when deleting the last todo (swapping `outerHTML` of a `<tr>` with a `<p>`), stale-object attribute writes on complete, unhandled Pydantic v2 `ValidationError` returning JSON 422 responses instead of HTML form errors, missing priority allowed-values validation, and profile form HTMX targets that reference the form container itself.

## What Changes

- Fix the delete-todo HTMX swap so the empty state renders as a `<p>` within the `<tbody>` (not as `outerHTML` of a `<tr>`).
- Fix the profile form HTMX target to use an inner container.
- Fix the complete-todo handler to load the fresh todo instance from storage before saving (no stale object attribute writes).
- Fix the delete-account handler to respect HTMX requests by returning HTML rather than a 302 redirect.
- Catch Pydantic v2 `ValidationError` in add/edit todo handlers so invalid input re-renders the form with HTML errors.
- Add allowed-values validation for the add-todo priority Form field (high/medium/low).
- Fix empty-string due-date handling in the edit-todo handler (empty string clears the due date).

## Capabilities

### Modified Capabilities

- `htmx-jinja2-frontend`: Delete/complete/edit/add todo HTMX behavior, empty-state rendering, and error handling.

## Impact

- Affected code: `snekdo/web.py`, `snekdo/templates/*.html`.
- No new dependencies.
- The CSRF token inclusion in forms is handled by the `web-csrf` child change.