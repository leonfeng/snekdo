## Context

See proposal.md — Why. Row fragments render from `list_row.html`/`list_rows.html`; profile/password forms live in `profile_content.html`; delete-account and password-change routes are in `snekdo/web.py`. Depends on the CSRF change having applied the hidden token input.

## Goals / Non-Goals

**Goals:**
- Every complete/delete HTMX interaction swaps with valid HTML and sibling rows stay interactive.
- Empty state after last-todo deletion is a `<p>` inside `<tbody>`.
- Profile/password forms target the inner container.
- Delete-account and password-change HTMX responses return HTML.

**Non-Goals:**
- No REST API or CLI changes.
- No CSRF logic (owned by the csrf change).
- No e2e test additions (owned by the e2e change).

## Decisions

- **Shared row fragment for swaps**: the complete/delete handlers render the same row fragment template as the initial list so the swapped row matches sibling structure. Rejected: ad-hoc per-action fragments (drift).
- **Empty state is a `<p>` inside `<tbody>`**: kept in `list_rows.html` and the fragment. Rejected: `outerHTML` of a `<tr>` (invalid HTML, breaks sibling wiring).
- **Profile/password target the inner container**: `hx-target` references an inner span/div within the form, not the form's wrapper. Rejected: targeting the wrapper (self-referential replacement loop).
- **HTMX responses return HTML, not 302**: the route checks the `HX-Request` header and renders HTML content back for the targeted swap. Rejected: redirect (full page reload, breaks in-place update).

## Risks / Trade-offs

- [Row fragment drift from the full list template] → Keep both rendered from the same row partial.
- [Returning HTML for HTMX while redirecting for normal posts changes two response shapes] → Branch only on the `HX-Request` header; non-HTMX posts still redirect.

## Migration Plan

In-place template/route fixes; rollback = revert. No data migration.

## Open Questions

- None.