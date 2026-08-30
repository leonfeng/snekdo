## 1. Web handlers

- [x] 1.1 Parse comma-separated tags input (split, trim, drop empties, dedupe preserving order) and category in `snekdo/web.py` add handler; store on the todo
- [x] 1.2 Parse tags and category in the web edit handler; empty category clears the field

## 2. Templates

- [x] 2.1 Add comma-separated `tags` and `category` inputs to `snekdo/templates/add.html`
- [x] 2.2 Add pre-filled `tags` (comma-joined) and `category` inputs to `snekdo/templates/edit.html`
- [x] 2.3 Add `Tags` and `Category` columns to `snekdo/templates/list.html` and the `list_row.html` partial

## 3. Tests

- [x] 3.1 Web tests: add form contains tags and category inputs; submitting them stores the parsed values on the todo
- [x] 3.2 Web tests: edit form pre-fills tags (comma-joined) and category; editing updates both
- [x] 3.3 Web tests: list view shows Tags and Category columns, empty cells when missing
