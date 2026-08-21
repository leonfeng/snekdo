## Context

See proposal.md — Why. The web frontend lives in `snekdo/web.py` (routes) and `snekdo/web_auth.py` (auth/session helper), rendered by Jinja2 templates in `snekdo/templates/` with HTMX partial updates. The REST API in `snekdo/api.py` and the CLI remain untouched. There is currently no CSRF module; state-changing HTML forms carry no tokens, and `web_auth.py` falls back to a static secret. `tests/e2e/` covers some auth flows but no security flows.

## Goals / Non-Goals

**Goals:**
- Per-session CSRF tokens, validated on HTML state-changing web endpoints only.
- No hardcoded/static default secrets in `web_auth.py`; no plaintext password logging.
- HTMX template interactions (complete/delete/last-row-empty-state, profile form targets) behave correctly and stay interactive across partial updates.
- E2e coverage for login/register/logout plus CSRF acceptance/rejection.

**Non-Goals:**
- No changes to the `/api/v1/*` REST endpoints, sync command, storage format, or CLI.
- No new web dependencies; keep HTMX via CDN and stdlib-only server code.
- No rate limiting, account lockout, or MFA.

## Decisions

- **CSRF via session-stored token + hidden form field** (`snekdo/csrf.py`). Token generated with `secrets.token_urlsafe()`, stored in the web session on first use, validated on form-encoded POSTs to state-changing routes. Alternatives considered: double-submit cookie (rejected — session already exists and is simpler to reuse) and per-request nonce (rejected — stateless, harder to test and harder to invalidate on logout).
- **CSRF bypass for JSON/HTMX requests**: requests with an `HX-Request` header (or JSON body) skip CSRF form-field validation and use the normal auth path. Rationale: the existing HTMX client does not send the hidden field, and forcing it would break the partial-update flows; CSRF protection applies to HTML form submissions where cross-origin forgery is the risk.
- **Secret sourced from env with random fallback**: `web_auth.py` reads its signing/secret key from an environment variable; when unset it generates a random per-process key instead of a static string. Rejected: keeping a static default (weak, shared across deployments).
- **Empty-state HTML stays a `<p>` inside `<tbody>`** rendered by the shared row templates, so last-row deletion does not emit invalid HTML or drop sibling rows' HTMX wiring.
- **E2e CSRF tests supply the token by scraping the hidden input** from the rendered form page (test client session), no new production code needed for tests.

## Risks / Trade-offs

- [JSON-path bypass widens attack surface if an HTML form ever submits JSON] → Keep the bypass limited to explicit `HX-Request`/JSON content-type; HTML form posts from our templates always carry the field.
- [Invalidating CSRF on logout means the token changes each session] → Expected behavior; tests assert a fresh session gets a usable new token after re-login.
- [Random per-process secret breaks token validation across workers] → Acceptable for single-process `snekdo serve`; deploying behind multiple workers requires setting the env secret explicitly (documented in tasks).

## Migration Plan

Deploy is additive: existing sessions simply pick up CSRF on first form render; no stored data changes. Rollback = revert the code; no schema or storage migration exists.

## Open Questions

- Whether `complete`/`delete` HTMX buttons should carry the CSRF token as a `hx-vals` attribute for hardening is deferred; current slice leaves the HTMX path on the JSON/HX bypass and the hidden-field contract unchanged.