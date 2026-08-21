## 1. HTMX rendering fixes

- [x] 1.1 Fix delete todo to target `<tbody>` instead of `<tr>` for empty state
- [x] 1.2 Fix profile form HTMX target to use an inner container
- [x] 1.3 Fix complete todo to load fresh instance before saving
- [x] 1.4 Fix delete account to handle HTMX requests (return HTML, not 302)

## 2. Form validation fixes

- [x] 2.1 Catch Pydantic v2 ValidationError in add_todo and edit_todo
- [x] 2.2 Add allowed-values validation for priority field (high/medium/low)
- [x] 2.3 Fix empty-string due-date handling in edit_todo