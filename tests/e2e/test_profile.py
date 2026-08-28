"""E2E tests for the profile page."""

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
        'return fetch(params.hxPostUrl, { method: "POST", headers: { "HX-Request": "true" }, body: fd })'
        '.then(r => r.text()).then(d => { document.getElementById("profile-content").innerHTML = d; return d; }); '
        '}',
        {'formSelector': form_selector, 'hxPostUrl': hx_post_url},
    )
    await page.wait_for_timeout(500)


async def test_view_profile(page):
    """A logged-in user can view their profile."""
    await page.goto(f"{BASE_URL}/profile")
    assert "Profile" in await _get_text(page)
    assert "Username" in await _get_text(page)


async def test_update_profile(page):
    """A user can update their display name and email."""
    await page.goto(f"{BASE_URL}/profile")
    await page.fill('input[name="display_name"]', "Test User")
    await page.fill('input[name="email"]', "test@example.com")
    await page.locator('button:has-text("Update Profile")').click()
    await page.wait_for_timeout(500)
    await page.goto(f"{BASE_URL}/profile")
    display_name = await page.locator('input[name="display_name"]').input_value()
    assert "Test User" in display_name


async def test_update_email_invalid(page):
    """An invalid email format shows an error."""
    await page.goto(f"{BASE_URL}/profile")
    await page.locator('input[name="display_name"]').clear()
    await page.fill('input[name="email"]', "not-an-email")
    await _htmx_submit(page, 'form[hx-post="/profile/update"]', '/profile/update', {})
    content = await page.evaluate('document.getElementById("profile-content").innerHTML')
    assert "invalid email format" in content.lower()


async def test_change_password_wrong_current(page):
    """Changing password with wrong current password shows an error."""
    await page.goto(f"{BASE_URL}/profile")
    await _htmx_submit(page, 'form[hx-post="/profile/password"]', '/profile/password', {
        'current_password': 'wrongpass',
        'new_password': 'newpassword123',
        'confirm_password': 'newpassword123',
    })
    content = await page.evaluate('document.getElementById("profile-content").innerHTML')
    assert "current password is incorrect" in content.lower()


async def test_change_password_success(page):
    """A user can change their password with valid data."""
    await page.goto(f"{BASE_URL}/profile")
    await _htmx_submit(page, 'form[hx-post="/profile/password"]', '/profile/password', {
        'current_password': 'password123',
        'new_password': 'newpass123',
        'confirm_password': 'newpass123',
    })
    await page.goto(f"{BASE_URL}/profile")
    current = await page.locator('#current_password').input_value()
    new = await page.locator('input[name="new_password"]').input_value()
    confirm = await page.locator('input[name="confirm_password"]').input_value()
    assert current == ""
    assert new == ""
    assert confirm == ""


async def test_change_password_short(page):
    """A short new password shows an error."""
    await page.goto(f"{BASE_URL}/profile")
    await _htmx_submit(page, 'form[hx-post="/profile/password"]', '/profile/password', {
        'current_password': 'password123',
        'new_password': 'short',
        'confirm_password': 'short',
    })
    content = await page.evaluate('document.getElementById("profile-content").innerHTML')
    assert "at least 8 characters" in content.lower()


async def test_change_password_mismatch(page):
    """Mismatched passwords show an error."""
    await page.goto(f"{BASE_URL}/profile")
    await _htmx_submit(page, 'form[hx-post="/profile/password"]', '/profile/password', {
        'current_password': 'password123',
        'new_password': 'newpass123',
        'confirm_password': 'different',
    })
    content = await page.evaluate('document.getElementById("profile-content").innerHTML')
    assert "passwords do not match" in content.lower()
