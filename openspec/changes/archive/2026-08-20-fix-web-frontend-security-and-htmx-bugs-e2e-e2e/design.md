## Context

See proposal.md — Why. The CSRF and HTMX slices have already been applied, so the web forms carry the CSRF token and the HTMX interactions render valid HTML. This change only adds verification under `tests/e2e/`.

## Goals / Non-Goals

**Goals:**
- E2e coverage for web registration, login, and logout through the real forms (with the CSRF token).
- E2e coverage for CSRF acceptance, missing-token and mismatched-token rejection (403), and token invalidation on logout.
- Assertion that no plaintext password appears in logs during register/login.

**Non-Goals:**
- No production code changes.
- No new spec requirements; this verifies existing behavior already described by the `user-auth` and `web-csrf-protection` capabilities.

## Decisions

- **Token scraping in conftest**: the helper parses the rendered form page for the hidden CSRF input and reuses it on follow-up posts, matching the single-session e2e browser flow. Rejected: bypassing CSRF in tests (would not exercise the real guard).
- **Log capture assertion**: e2e tests capture server logs and assert the plaintext password string is absent. Rejected: only checking the stored record (insufficient to catch logging leaks).

## Risks / Trade-offs

- [Flaky log capture across runners] → Scope the assertion to the specific test's captured log buffer.
- [CSRF token scraping breaks if form markup changes] → The helper reads a stable hidden-input name; keep the input name consistent with the CSRF change.

## Migration Plan

Tests only; rollback = remove the added test files. No production impact.

## Open Questions

- None.