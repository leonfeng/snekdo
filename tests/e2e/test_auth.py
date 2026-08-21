"""E2E tests for the authentication flow."""

import pytest

pytestmark = [pytest.mark.e2e, pytest.mark.asyncio]

BASE_URL = "http://127.0.0.1:8765"


async def _get_text(page):
    return await page.locator('body').text_content()


async def _get_csrf_token(page):
    """Get the current CSRF token from the page's cookie."""
    cookies = await page.context.cookies()
    for cookie in cookies:
        if cookie['name'] == 'csrf_token':
            return cookie['value']
    return None


async def test_registration_success(page):
    """A new user can register and log in."""
    await page.context.clear_cookies()
    await page.goto(f"{BASE_URL}/auth/register")
    await page.fill('input[name="username"]', "testuser2")
    await page.fill('input[name="password"]', "password123")
    csrf_token = await _get_csrf_token(page)
    await page.evaluate(
        "(csrf) => { "
        "const form = document.querySelector('form'); "
        "const input = form.querySelector('input[name=\"csrf_token\"]'); "
        "if (input) input.value = csrf; "
        "document.querySelector('form').submit(); }",
        csrf_token,
    )
    await page.wait_for_url(f"{BASE_URL}/auth/login")
    assert page.url.startswith(BASE_URL)

    await page.goto(f"{BASE_URL}/auth/login")
    await page.fill('input[name="username"]', "testuser2")
    await page.fill('input[name="password"]', "password123")
    csrf_token2 = await _get_csrf_token(page)
    await page.evaluate(
        "(csrf) => { "
        "const form = document.querySelector('form'); "
        "const input = form.querySelector('input[name=\"csrf_token\"]'); "
        "if (input) input.value = csrf; "
        "document.querySelector('form').submit(); }",
        csrf_token2,
    )
    await page.wait_for_url(BASE_URL)
    assert "Todos" in await _get_text(page)


async def test_registration_with_invalid_data(page):
    """Registration with an empty username shows an error."""
    await page.context.clear_cookies()
    await page.goto(f"{BASE_URL}/auth/register")
    await page.fill('input[name="username"]', "")
    await page.fill('input[name="password"]', "password123")
    csrf_token = await _get_csrf_token(page)
    await page.evaluate(
        "(csrf) => { "
        "const form = document.querySelector('form'); "
        "const input = form.querySelector('input[name=\"csrf_token\"]'); "
        "if (input) input.value = csrf; "
        "document.querySelector('form').submit(); }",
        csrf_token,
    )
    await page.wait_for_load_state("domcontentloaded")
    error_text = (await page.locator(".error").text_content() or "").lower()
    assert "username must be at least 3 characters" in error_text


async def test_login_success(page):
    """A user can log in with valid credentials."""
    await page.context.clear_cookies()
    await page.goto(f"{BASE_URL}/auth/login")
    await page.fill('input[name="username"]', "testuser")
    await page.fill('input[name="password"]', "password123")
    csrf_token = await _get_csrf_token(page)
    await page.evaluate(
        "(csrf) => { "
        "const form = document.querySelector('form'); "
        "const input = form.querySelector('input[name=\"csrf_token\"]'); "
        "if (input) input.value = csrf; "
        "document.querySelector('form').submit(); }",
        csrf_token,
    )
    await page.wait_for_url(BASE_URL)
    assert "Todos" in await _get_text(page)


async def test_login_with_invalid_credentials(page):
    """Login with invalid credentials shows an error."""
    await page.context.clear_cookies()
    await page.goto(f"{BASE_URL}/auth/login")
    await page.fill('input[name="username"]', "wronguser")
    await page.fill('input[name="password"]', "wrongpass")
    csrf_token = await _get_csrf_token(page)
    await page.evaluate(
        "(csrf) => { "
        "const form = document.querySelector('form'); "
        "const input = form.querySelector('input[name=\"csrf_token\"]'); "
        "if (input) input.value = csrf; "
        "document.querySelector('form').submit(); }",
        csrf_token,
    )
    assert "Incorrect username or password" in await _get_text(page)


async def test_logout(page):
    """A logged-in user can log out."""
    await page.goto(f"{BASE_URL}/todos")
    await page.click('button.logout')
    await page.wait_for_url(f"{BASE_URL}/auth/login")
    assert "Login" in await _get_text(page)
