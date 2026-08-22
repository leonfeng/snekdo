## Context

The web frontend's todo list (`snekdo/templates/list.html`) currently displays all todos in a table. Completed todos are marked with a "✓" status. There is no mechanism to collapse/expand completed todos. The HTMX library is loaded via CDN in `base.html`, and the project avoids any npm/build dependencies.

The completed todos count can be obtained from the template context (the `todos` list contains both completed and pending items).

## Goals / Non-Goals

**Goals:**
- Add a collapsible section above the todo table that shows the count of completed todos
- Include a caret icon that indicates expand/collapse state
- When expanded, display the list of completed todo items below the heading
- When collapsed, hide the completed todos list
- Use only HTML/CSS/HTMX - no JavaScript framework or build step required
- Maintain responsive design and existing table styling

**Non-Goals:**
- No server-side API changes needed - completed todos are already accessible
- No changes to the backend storage or API
- No new CLI commands or flags
- No database schema changes

## Decisions

### Decision: Client-side collapsible using details/summary HTML elements

**Choice**: Use the native HTML `<details>` and `<summary>` elements for the collapsible functionality, styled with CSS and optionally enhanced with HTMX attributes.

**Rationale**:
- Native HTML elements require no JavaScript, aligning with the project's "no build step" philosophy
- `<details>/<summary>` provides built-in expand/collapse behavior and keyboard accessibility
- The `<summary>` element can contain custom content including the heading with count and caret icon
- No additional dependencies or HTMX interactions needed on the server side

**Alternatives considered**:
- Custom JavaScript toggle - requires JS code and event handlers, contradicts "no build step" goal
- HTMX-only approach with `hx-on` attributes - possible but less semantic than native elements
- React/Vue component - requires build step and new dependencies, rejected

### Decision: Caret icon via CSS pseudo-element

**Choice**: Use a CSS pseudo-element (`::after`) on the `<summary>` to display a caret icon that rotates based on the open state.

**Rationale**:
- No additional image assets or font files needed
- CSS alone can handle the rotation animation
- Keeps the HTML clean and semantic

**Alternatives considered**:
- Image sprite - requires asset management
- Font Awesome icon - requires external dependency
- Emoji character (`▲`/`▼`) - simpler but less visually polished

### Decision: Completed todos display format

**Choice**: When expanded, completed todos are displayed in an unordered list below the collapsible heading, showing each todo's title and ID.

**Rationale**:
- Clean separation from the main table
- Easy to read and scan
- Consistent with the existing list display style
- Uses existing todo data (title, ID) already available in the template context

**Alternatives considered**:
- Inline within the table - would require table restructuring
- Modal popup - additional interaction, less accessible

## Risks / Trade-offs

**Risk**: Native `<details>/<summary>` may not style consistently across all browsers.

**Mitigation**: Test on Chrome, Firefox, and Safari. Add fallback CSS for basic styling.

**Risk**: The count `{n}` must be computed at render time from the template context.

**Mitigation**: The Jinja2 template already has access to the `todos` list; counting completed items is straightforward.

**Risk**: CSS rotations may not work in very old browsers.

**Mitigation**: Provide a simple non-rotating caret as fallback using `@supports`.

## Migration Plan

No migration required - this is a new UI element added to the existing web interface. Existing todos and their completed status are preserved.
