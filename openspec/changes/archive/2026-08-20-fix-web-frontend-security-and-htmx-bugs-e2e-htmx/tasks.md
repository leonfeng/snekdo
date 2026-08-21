## 1. Row swap fragments

- [ ] 1.1 Fix `snekdo/templates/list_row.html` / `list_rows.html` so a completed or deleted row swaps with valid HTML and sibling rows keep their HTMX wiring

## 2. Empty state

- [ ] 2.1 Render the empty state after deleting the last todo as a `<p>` element inside the `<tbody>` (never `outerHTML` of a `<tr>`)

## 3. Profile form targets

- [ ] 3.1 Fix the profile update and password change form HTMX targets to reference the inner container, not the form's own wrapper

## 4. Delete-account / password-change responses

- [ ] 4.1 Make the delete-account route return HTML content (not a 302 redirect) when the request is HTMX
- [ ] 4.2 Make the password-change route return HTML content (not a 302 redirect) when the request is HTMX

## 5. Verification

- [ ] 5.1 Confirm complete and delete interactions render valid HTML and that the remaining rows stay interactive after a partial update