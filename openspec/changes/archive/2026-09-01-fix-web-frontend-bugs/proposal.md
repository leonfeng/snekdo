## Why

The web frontend has several bugs that break the user experience:
HTMX partial templates (`list_row.html`, `list_rows.html`) render fewer table
columns than the main `list.html` table, causing column misalignment after
Complete or Delete actions. The detail page (`show.html`) omits the Tags and
Category fields. The confirmation page inherits a nav bar that links to
authenticated-only routes after the user is logged out. The `success-message`
CSS class used on the confirmation page has no corresponding CSS rule.

## What Changes

- Add Repeat, Tags, and Category columns to `list_row.html` so the HTMX
  single-row swap matches the 10-column table in `list.html`.
- Add Repeat, Tags, and Category columns to `list_rows.html` so the HTMX
  full-row swap after delete matches the table structure.
- Add Tags and Category display sections to `show.html`.
- Make the confirmation page standalone (no nav bar / no auth-dependent
  links) so it does not show stale navigation after account deletion.
- Add a `.success-message` CSS class to `base.html` so the confirmation
  page's success message is styled.
- Update e2e tests to verify the new columns and fix the confirmation page
  assertions.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `htmx-jinja2-frontend`: List rows, detail page, and confirmation page
  must display all todo fields consistently; confirmation page must not show
  authenticated navigation.

## Impact

- `snekdo/templates/list_row.html` — add Repeat, Tags, Category cells.
- `snekdo/templates/list_rows.html` — add Repeat, Tags, Category cells.
- `snekdo/templates/show.html` — add Tags and Category display sections.
- `snekdo/templates/confirmation.html` — make standalone (no nav) or
  conditionally hide nav.
- `snekdo/templates/base.html` — add `.success-message` CSS rule.
- `tests/test_e2e_web.py` — update column-count assertions, add
  assertions for new columns, fix confirmation page assertions.
