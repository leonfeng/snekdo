## Why

The web frontend's todo list currently shows all todos including completed ones, which creates visual noise when users want to focus on pending tasks. A collapsible section for completed todos would allow users to expand and view completed items on demand.

## What Changes

- Add a collapsible UI element to the web todo list that displays the count of completed todos in the heading (`{n} completed todos`)
- When clicked, the collapsible expands to show the list of completed todo items
- When clicked again while expanded, the collapsible contracts and hides the list
- Include a caret icon next to the heading to indicate expand/collapse state

## Capabilities

### New Capabilities

- `web-collapsible-completed`: Adds a collapsible UI element in the web frontend to display and toggle visibility of completed todos. This capability introduces new template modifications and HTMX interaction patterns.

### Modified Capabilities

- `list-display`: The list template now includes a collapsible completed todos section alongside the existing table.

## Impact

- **Templates**: `snekdo/templates/list.html` - adds collapsible completed todos section
- **CSS**: Enhanced styling in `snekdo/templates/base.html` for caret icon and collapsible state
- **HTMX**: No server-side changes needed; interaction is handled client-side
- **Backend**: No API changes; completed todos are already stored and accessible
