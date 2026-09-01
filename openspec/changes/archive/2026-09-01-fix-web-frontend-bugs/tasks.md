## 1. Fix HTMX partial templates (column alignment)

- [x] 1.1 Add Repeat, Tags, and Category cells to `snekdo/templates/list_row.html` matching the column order in `list.html` (Repeat after Due, then Created At, Tags, Category before Actions)
- [x] 1.2 Add Repeat, Tags, and Category cells to `snekdo/templates/list_rows.html` matching the column order in `list.html`

## 2. Fix show.html missing fields

- [x] 2.1 Add a "Repeat" detail-group to `snekdo/templates/show.html` showing the repeat value (or "—" if none)
- [x] 2.2 Add a "Tags" detail-group to `snekdo/templates/show.html` showing comma-joined tags (or "—" if empty)
- [x] 2.3 Add a "Category" detail-group to `snekdo/templates/show.html` showing the category (or "—" if empty)

## 3. Fix confirmation page

- [x] 3.1 Make `snekdo/templates/confirmation.html` a standalone page (remove `{% extends "base.html" %}`) with its own HTML structure, minimal styling, and a link to `/auth/login`
- [x] 3.2 Add a `.success-message` CSS rule to `snekdo/templates/base.html` (green background, padding, border-radius) so it is available if any other page uses it in the future

## 4. Update e2e tests

- [x] 4.1 Update `tests/test_e2e_web.py` to assert the correct column count (10 columns: ID, Title, Status, Priority, Due, Repeat, Created At, Tags, Category, Actions) in list rows
- [x] 4.2 Add an e2e test verifying that after completing a todo via HTMX, the updated row still has the correct number of cells
- [x] 4.3 Add an e2e test verifying that after deleting a todo via HTMX, remaining rows have the correct number of cells
- [x] 4.4 Update any confirmation page assertions to expect a standalone page (no nav links to /todos or /profile)

## 5. Verify

- [x] 5.1 Run the full test suite (`uv run pytest`) and confirm all tests pass
