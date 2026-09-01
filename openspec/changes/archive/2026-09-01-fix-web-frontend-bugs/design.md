## Context

The web frontend uses Jinja2 templates with HTMX for partial page updates. The main list view (`list.html`) renders a 10-column table (ID, Title, Status, Priority, Due, Repeat, Created At, Tags, Category, Actions), but the HTMX partial templates (`list_row.html`, `list_rows.html`) only render 6 columns. This causes column misalignment after HTMX swaps.

The show page (`show.html`) is missing tags and category fields that are shown in the list view.

The confirmation page inherits from `base.html` which includes a nav bar with links to authenticated routes — inappropriate after logout.

## Goals / Non-Goals

**Goals:**
- Fix column alignment in `list_row.html` and `list_rows.html` by adding Repeat, Tags, and Category cells
- Display Tags and Category on the show (detail) page
- Remove auth-dependent navigation from the confirmation page
- Add missing CSS class for success message styling

**Non-Goals:**
- No changes to API, models, or storage layers
- No changes to authentication flow
- No changes to HTMX behavior or routing

## Decisions

### 1. Add missing columns to partial templates

**Decision:** Add Repeat, Tags, and Category `<td>` cells to both `list_row.html` and `list_rows.html`, matching the column order in `list.html`.

**Rationale:** The simplest fix that keeps the HTMX swap contract consistent. The templates already have access to `todo.repeat`, `todo.tags`, and `todo.category` via the Todo model.

### 2. Show page: add Tags and Category sections

**Decision:** Add two `<div class="detail-group">` blocks to `show.html` for Tags and Category, matching the existing pattern.

**Rationale:** Consistent with the existing detail-group pattern in the template.

### 3. Confirmation page: standalone template

**Decision:** Make `confirmation.html` a standalone page (not extending `base.html`) with its own minimal HTML structure.

**Rationale:** After account deletion the session is destroyed; showing nav links to `/todos`, `/todos/add`, `/profile` would 401/redirect and confuse the user. A standalone page with just the success message and a link to register/login is cleaner.

### 4. Add `.success-message` CSS

**Decision:** Add a `.success-message` CSS class to `base.html` styles with a green-tinted background, padding, and border-radius.

**Alternative considered:** Inline styles in the template — rejected because it's inconsistent with the rest of the styling approach.

## Risks / Trade-offs

- [Risk] E2E tests may depend on exact column counts — must update assertions to match new column count (10 columns).
  - Mitigation: Update test assertions in `tests/test_e2e_web.py` to match.
- [Risk] Changing `confirmation.html` from extending `base.html` to standalone means it loses the `<style>` block — must include minimal styling inline or in a small style block.
  - Mitigation: Inline minimal CSS in the confirmation template.
