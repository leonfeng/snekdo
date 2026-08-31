"""E2E tests for the web frontend security features.

Covers: CSRF token presence in forms, rejecting invalid CSRF,
auth redirect for unauthenticated access, and account deletion via HTMX.

These tests require a running server (started by the test fixture)
and a browser (Playwright).

Usage:
    SNEKDO_STORAGE_PATH=/tmp/snekdo-e2e/todos.json \
    SNEKDO_USERS_PATH=/tmp/snekdo-e2e/users.json \
    uv run pytest tests/e2e/ -m e2e -v
"""

import pytest
import pytest_asyncio

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
    """Fill form fields and submit via fetch with HTMX-style request."""
    csrf_token = await _get_csrf_token(page)
    for name, value in fill_values.items():
        await page.locator(f'{form_selector} input[name="{name}"]').fill(value)
    return await page.evaluate(
        """(params) => {
            const form = document.querySelector(params.formSelector);
            const fd = new FormData(form);
            return fetch(params.hxPostUrl, {
                method: 'POST',
                headers: { 'HX-Request': 'true', 'X-CSRF-Token': params.csrfToken },
                body: fd,
                credentials: 'include',
            }).then(r => r.text());
        }""",
        {'formSelector': form_selector, 'hxPostUrl': hx_post_url, 'csrfToken': csrf_token},
    )


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
    # Use fetch directly with a known-wrong token to trigger CSRF rejection
    body = await page.evaluate(
        """() => {
            return fetch('/todos/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: 'title=Test+todo&csrf_token=wrong-token-value',
                credentials: 'include'
            }).then(r => r.text());
        }"""
    )
    assert body is not None
    assert "invalid csrf token" in body.lower()


async def test_no_state_mutation_on_csrf_rejection(page):
    """No state mutation on CSRF rejection: todo count should not change."""
    await page.goto(f"{BASE_URL}/todos")
    todos_before = await page.locator('.todo-row').count()
    await page.goto(f"{BASE_URL}/todos/add")
    await page.fill('input[name="title"]', "Test todo no mutation")
    # Remove CSRF token to trigger rejection
    await page.evaluate(
        '() => { const i = document.querySelector(\'input[name="csrf_token"]\'); if (i) i.remove(); }'
    )
    await page.evaluate(
        '() => { document.querySelector(\'form[action="/todos/add"]\').submit(); }'
    )
    await page.wait_for_load_state("load")
    # Verify no new todo was created by navigating to the list
    await page.goto(f"{BASE_URL}/todos")
    todos_after = await page.locator('.todo-row').count()
    assert todos_before == todos_after


async def test_csrf_token_invalidated_on_logout(page):
    """CSRF token invalidated on logout: resubmitting the pre-logout token is rejected."""
    await page.goto(f"{BASE_URL}/todos")
    old_token = await _get_csrf_token(page)
    assert old_token is not None

    # Log out
    await page.click('form[action="/auth/logout"] button[type="submit"]')
    await page.wait_for_url(f"{BASE_URL}/auth/login")

    # Log back in — a new CSRF token is issued
    await page.goto(f"{BASE_URL}/auth/login")
    await page.fill('input[name="username"]', "testuser")
    await page.fill('input[name="password"]', "password123")
    await page.click('button[type="submit"]')
    await page.wait_for_url(BASE_URL)

    # Now submit to /todos/add with the OLD (invalidated) CSRF token via fetch
    await page.goto(f"{BASE_URL}/todos/add")
    body = await page.evaluate(
        """(oldToken) => {
            return fetch('/todos/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: 'title=Test+csrf+after+logout&csrf_token=' + encodeURIComponent(oldToken),
                credentials: 'include',
            }).then(r => r.text());
        }""",
        old_token,
    )
    assert body is not None
    assert "invalid csrf token" in body.lower()


async def test_delete_account_via_htmx(page):
    """Deleting the account via HTMX removes the account and shows login."""
    await page.goto(f"{BASE_URL}/profile")
    body = await _htmx_submit(page, 'form[hx-post="/profile/delete"]', '/profile/delete', {
        'current_password': 'password123',
    })
    await page.wait_for_timeout(500)
    # The HTMX response is the confirmation page
    assert "deleted" in body.lower()
