# Proposal: Tags & Categories — Web UI

## Why

The REST API and CLI now support `tags` and `category`, but the web frontend (Jinja2 + HTMX) does not let users see or set them. This slice adds form inputs and list columns so the feature is usable in the browser.

## What Changes

- Add form (`add.html` + web handler): new comma-separated `tags` input and `category` input; handler parses and stores them.
- Edit form (`edit.html` + web handler): same inputs pre-filled from the existing todo; handler updates both fields.
- List view (`list.html` / `list_rows.html`): new `Tags` and `Category` columns.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `htmx-jinja2-frontend`: add/edit forms include `tags` and `category` inputs; list view shows both columns.

## Impact

- `snekdo/web.py`: add/edit handlers parse the new form fields.
- `snekdo/templates/add.html`, `edit.html`, `list.html`, `list_rows.html`: new inputs and columns.
- Tests: `tests/test_web.py` for form inputs and list columns.
