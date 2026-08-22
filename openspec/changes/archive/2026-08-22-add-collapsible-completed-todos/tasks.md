## 1. Modify list.html template

- [x] 1.1 Add `<details>` and `<summary>` elements around the todo table in `snekdo/templates/list.html`
- [x] 1.2 Add collapsible heading with completed count `{n} completed todos` and caret icon in the `<summary>` element
- [x] 1.3 Add completed todos list inside the `<details>` element when expanded, displaying each completed todo's title and ID
- [x] 1.4 Ensure the collapsible integrates with existing table styling in `base.html`

## 2. Verify design decisions

- [x] 2.1 Confirm `<details>/<summary>` native HTML approach meets requirements
- [x] 2.2 Verify CSS caret icon styling works with existing base.html styles
- [x] 2.3 Test collapsible behavior (expand/collapse) in browsers

## 3. Run tests to verify

- [x] 3.1 Run `pytest` to ensure existing tests still pass
- [x] 3.2 Verify the web frontend renders correctly with the new collapsible element
