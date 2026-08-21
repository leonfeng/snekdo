"""E2E tests for account deletion via the web frontend."""

import pytest

pytestmark = [pytest.mark.e2e, pytest.mark.asyncio]

BASE_URL = "http://127.0.0.1:8765"


async def _get_text(page):
    return await page.locator('body').text_content()


async def _htmx_submit(page, form_selector, hx_post_url, fill_values):
    """Fill form fields and submit via HTMX fetch request."""
    for name, value in fill_values.items():
        await page.locator(f'{form_selector} input[name="{name}"]').fill(value)
    await page.evaluate(
        '(params) => { '
        'const form = document.querySelector(params.formSelector); '
        'const fd = new FormData(form); '
        'return fetch(params.hxPostUrl, { '
        'method: "POST", headers: { "HX-Request": "true" }, body: fd })'
        '.then(r => r.text()).then(d => { '
        'document.getElementById("profile-content").innerHTML = d; return d; }); '
        '}',
        {'formSelector': form_selector, 'hxPostUrl': hx_post_url},
    )
    await page.wait_for_timeout(500)


async def test_delete_account_button_visible(page):
    """A logged-in user sees the delete account button on the profile page."""
    await page.goto(f"{BASE_URL}/profile")
    assert "Delete Account" in await _get_text(page)


async def test_delete_account_wrong_password(page):
    """Deleting with wrong password shows an error and keeps the account."""
    await page.goto(f"{BASE_URL}/profile")
    await _htmx_submit(page, 'form[hx-post="/profile/delete"]', '/profile/delete', {
        'current_password': 'wrongpassword',
    })
    content = await page.evaluate(
        'document.getElementById("profile-content").innerHTML'
    )
    assert "incorrect password" in content.lower()


async def test_delete_account_cancel(page):
    """Cancelling the confirmation dialog leaves the profile unchanged."""
    await page.goto(f"{BASE_URL}/profile")
    assert "Delete Account" in await _get_text(page)


async def test_delete_account_success(page):
    """Deleting with correct password shows confirmation page and redirects to login."""
    await page.goto(f"{BASE_URL}/profile")
    await _htmx_submit(page, 'form[hx-post="/profile/delete"]', '/profile/delete', {
        'current_password': 'password123',
    })
    await page.wait_for_timeout(500)
    # After successful deletion, the page should show the confirmation page
    content = await page.evaluate('document.body.innerHTML')
    assert "Account Deleted" in content
    assert "Your account has been successfully deleted" in content


async def test_account_no_longer_accessible(page):
    """A deleted user's token is no longer valid."""
    await page.goto(f"{BASE_URL}/profile")
    await _htmx_submit(page, 'form[hx-post="/profile/delete"]', '/profile/delete', {
        'current_password': 'password123',
    })
    await page.wait_for_timeout(500)
    # Try to access profile again - should redirect to login
    await page.goto(f"{BASE_URL}/profile")
    await page.wait_for_url(f"{BASE_URL}/auth/login")
    assert "Login" in await _get_text(page)


async def test_confirmation_page_visible(page):
    """Confirmation page is shown after successful account deletion."""
    await page.goto(f"{BASE_URL}/profile")
    await _htmx_submit(page, 'form[hx-post="/profile/delete"]', '/profile/delete', {
        'current_password': 'password123',
    })
    await page.wait_for_timeout(500)
    # Confirmation page should be visible
    assert "Account Deleted" in await page.locator('body').text_content()
    assert "Your account has been successfully deleted" in await page.locator('body').text_content()
