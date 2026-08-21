## Context

See proposal.md — Why. `snekdo/web.py` renders the HTML web frontend; `snekdo/web_auth.py` handles auth/session and currently falls back to a static secret; there is no CSRF module. The REST API (`snekdo/api.py`) must remain untouched.

## Goals / Non-Goals

**Goals:**
- Per-session CSRF tokens issued and validated on HTML state-changing web endpoints.
- JSON/`HX-Request` requests bypass CSRF validation; REST API behavior unchanged.
- No static default secret; no plaintext password logging.

**Non-Goals:**
- No HTMX interaction/template-behavior fixes (separate change).
- No e2e coverage addition (separate change).
- No changes to storage format or CLI.

## Decisions

- **Session-stored token + hidden form field** in `snekdo/csrf.py`. `secrets.token_urlsafe()`, get-or-create per session, validated on form-encoded POSTs. Alternatives: double-submit cookie (rejected — session exists; simpler to reuse), per-request nonce (rejected — stateless, harder to invalidate on logout).
- **Bypass for JSON/HX requests**: CSRF check applies only to form-encoded HTML posts; JSON/`HX-Request` requests use the normal auth path. Rejected: forcing the token onto HTMX JSON requests (breaks existing partial-update client).
- **Secret from env, random fallback**: `web_auth.py` reads from an env var; unset → random per-process key. Rejected: static default (shared-secret weakness).

## Risks / Trade-offs

- [JSON bypass widens surface if an HTML form submits JSON] → Keep bypass limited to explicit content-type; our templates always send the field.
- [Token changes per session after logout] → Expected; re-login issues a fresh token.
- [Random per-process secret breaks multi-worker token signing] → Acceptable for single-process `snekdo serve`; multi-worker deploys set the env secret.

## Migration Plan

Additive; no data migration. Rollback = revert code.

## Open Questions

- None.