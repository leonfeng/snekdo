## Context

The Delete Account flow currently replaces the Profile Information form with the Login form after deletion, but leaves the rest of the Profile page visible. This design addresses showing a proper confirmation page instead.

## Goals / Non-Goals

**Goals:**
- Display a confirmation page after successful account deletion
- Redirect user to login page after viewing the confirmation

**Non-Goals:**
- Modifying the actual delete account API or storage logic
- Changing user authentication flow

## Decisions

- Create a dedicated confirmation template/page that shows deletion success message
- Route user to login after confirmation page is viewed
- Keep existing delete account API unchanged

## Risks / Trade-offs

- [Risk] User might not see the confirmation before redirect
  - [Mitigation] Keep confirmation visible for a reasonable time before redirect

## Open Questions

None
