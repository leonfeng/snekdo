## Why

After clicking the Delete Account button, the Profile Information form is replaced by the Login form, but the rest of the Profile page remains visible instead of showing a confirmation page that the account has been successfully deleted.

## What Changes

- **Behavioral change**: The delete account flow should display a confirmation page after successful deletion instead of showing the Login form with residual Profile page content.
- **User experience**: User should see a dedicated confirmation page stating their account has been successfully deleted.

## Capabilities

### New Capabilities

- `account-deletion`: Capability for handling account deletion with proper confirmation flow. This will include:
  - A confirmation page shown after account deletion
  - Proper redirection to login after confirmation

### Modified Capabilities

- None

## Impact

- Front-end: Profile page delete handler, confirmation page component
- Back-end: Delete account API endpoint, session cleanup
- No API contract changes, but flow behavior changes
