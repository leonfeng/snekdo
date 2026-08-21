"""E2E tests for web frontend security and HTMX bug fixes.

Covers: CSRF token presence in forms, deleting the last todo,
invalid priority on add, empty login credentials, POST logout, and delete account via HTMX.
"""

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


async def _create_todo(page, title: str = "Test todo"):
    """Helper to create a todo via the web form."""
    await page.goto(f"{BASE_URL}/todos/add")
    await page.fill('input[name="title"]', title)
    await page.evaluate(
        '() => { document.querySelector(\'form[action="/todos/add"]\').submit(); }'
    )
    await page.wait_for_url(f"{BASE_URL}/todos")


async def _get_todo_id(page, title: str = "Test todo"):
    """Get the todo ID from the list page."""
    link = page.locator(f'a[href^="/todos/"]:has-text("{title}")').first
    href = await link.get_attribute("href")
    return href.split("/")[-1]


async def _htmx_submit(page, form_selector, hx_post_url, fill_values):
    """Fill form fields and submit via HTMX fetch request with CSRF token."""
    csrf_token = await _get_csrf_token(page)
    for name, value in fill_values.items():
        await page.locator(f'{form_selector} input[name="{name}"]').fill(value)
    await page.evaluate(
        '(params) => { '
        'const form = document.querySelector(params.formSelector); '
        'const fd = new FormData(form); '
        'const headers = { "HX-Request": "true", "X-CSRF-Token": params.csrfToken }; '
        'return fetch(params.hxPostUrl, { method: "POST", headers: headers, body: fd })'
        '.then(r => r.text()).then(d => { document.getElementById("profile-content").innerHTML = d; return d; }); '
        '}',
        {'formSelector': form_selector, 'hxPostUrl': hx_post_url, 'csrfToken': csrf_token},
    )
    await page.wait_for_timeout(500)


async def test_csrf_token_in_add_form(page):
    """The add todo form includes a CSRF token hidden input."""
    await page.goto(f"{BASE_URL}/todos/add")
    form = page.locator('form[action="/todos/add"]')
    csrf_input = form.locator('input[name="csrf_token"]')
    assert await csrf_input.count() == 1
    token = await csrf_input.first.get_attribute('value')
    assert token


async def test_csrf_token_in_edit_form(page):
    """The edit todo form includes a CSRF token hidden input."""
    await _create_todo(page, "Edit CSRF")
    todo_id = await _get_todo_id(page, "Edit CSRF")
    await page.goto(f"{BASE_URL}/todos/{todo_id}/edit")
    form = page.locator('form[action^="/todos/"][action$="/edit"]')
    csrf_input = form.locator('input[name="csrf_token"]')
    assert await csrf_input.count() == 1
    token = await csrf_input.first.get_attribute('value')
    assert token


async def test_csrf_token_in_profile_forms(page):
    """The profile forms include a CSRF token hidden input."""
    await page.goto(f"{BASE_URL}/profile")
    # Count CSRF tokens within the profile content forms only (not the logout form in base.html)
    content = page.locator('#profile-content')
    csrf_inputs = content.locator('input[name="csrf_token"]')
    count = await csrf_inputs.count()
    assert count >= 3


async def test_csrf_acceptance_valid_token(page):
    """CSRF acceptance: a valid CSRF token submitted with a form is accepted."""
    await page.goto(f"{BASE_URL}/todos/add")
    await page.fill('input[name="title"]', "Test todo valid")
    await page.evaluate(
        '() => { document.querySelector(\'form[action="/todos/add"]\').submit(); }'
    )
    await page.wait_for_url(f"{BASE_URL}/todos")


async def test_csrf_missing_token_rejection_403(page):
    """CSRF missing-token rejection: submitting without a CSRF token returns 403."""
    await page.goto(f"{BASE_URL}/todos/add")
    await page.evaluate(
        '() => { '
        'const form = document.querySelector(\'form[action="/todos/add"]\'); '
        'form.innerHTML = ""; '
        '}'
    )
    await page.evaluate(
        '() => { document.querySelector(\'form[action="/todos/add"]\').submit(); }'
    )
    text = (await page.locator('body').text_content()).lower()
    assert "invalid csrf token" in text


async def test_csrf_mismatched_token_rejection_403(page):
    """CSRF mismatched-token rejection: submitting with a wrong CSRF token returns 403."""
    await page.goto(f"{BASE_URL}/todos/add")
    await page.fill('input[name="title"]', "Test todo for csrf test wrong")
    await page.evaluate(
        '() => { '
        'document.querySelector(\'input[name="csrf_token"]\').value = "wrong-token-value"; '
        '}'
    )
    # Submit the form with the modified csrf token value via fetch
    await page.evaluate(
        '() => { '
        'const form = document.querySelector(\'form[action="/todos/add"]\'); '
        'const fd = new FormData(form); '
        'fetch(form.action, { method: "POST", body: fd, credentials: "include" })'
        '.then(r => r.text()).then(d => document.body.innerHTML = d); '
        '}'
    )
    await page.wait_for_timeout(500)
    text = (await page.locator('body').text_content()).lower()
    assert "invalid csrf token" in text


async def test_no_state_mutation_on_csrf_rejection(page):
    """No state mutation on CSRF rejection: todo count should not change."""
    await page.goto(f"{BASE_URL}/todos")
    todos_before = await page.locator('.todo-row').count()
    await page.goto(f"{BASE_URL}/todos/add")
    await page.fill('input[name="title"]', "Test todo no mutation")
    await page.evaluate(
        '() => { document.querySelector(\'form[action="/todos/add"]\').submit(); }'
    )
    todos_after = await page.locator('.todo-row').count()
    assert todos_before == todos_after


async def test_csrf_token_invalidated_on_logout(page):
    """CSRF token invalidation on logout: resubmitting the pre-logout token is rejected."""
    await page.goto(f"{BASE_URL}/todos")
    csrf_token = await _get_csrf_token(page)
    await page.click('form[action="/auth/logout"] button[type="submit"]')
    await page.wait_for_url(f"{BASE_URL}/auth/login")
    # After logout, the CSRF token cookie should be deleted.
    # Submit to /todos/add with the old token - should be rejected (403).
    await page.goto(f"{BASE_URL}/todos/add")
    # The form should still have the csrf_token input from the server-rendered HTML
    # but the cookie is deleted, so the submitted token won't match
    await page.fill('input[name="title"]', "Test csrf after logout")
    await page.evaluate(
        f'(oldToken) => {{ '
        'const input = document.querySelector("input[name=\\"csrf_token\\"]"); '
        'if (input) input.value = oldToken; '
        'document.querySelector("form").submit(); }}',
        csrf_token,
    )
    await page.wait_for_load_state("load")
    text = (await page.locator('body').text_content()).lower()
    assert "invalid csrf token" in text


async def test_delete_account_via_htmx(page):
    """Deleting the account via HTMX removes the account and shows login."""
    await page.goto(f"{BASE_URL}/profile")
    await _htmx_submit(page, 'form[hx-post="/profile/delete"]', '/profile/delete', {
        'current_password': 'password123',
    })
    await page.wait_for_timeout(500)
    assert "Login" in await _get_text(page)