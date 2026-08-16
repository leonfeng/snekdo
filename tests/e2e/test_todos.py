"""E2E tests for the todo CRUD operations."""

import pytest

pytestmark = [pytest.mark.e2e, pytest.mark.asyncio]

BASE_URL = "http://127.0.0.1:8765"


async def _get_text(page):
    return await page.locator('body').text_content()


async def _create_todo(page, title: str = "Test todo"):
    """Helper to create a todo via the web form."""
    await page.goto(f"{BASE_URL}/todos/add")
    await page.fill('input[name="title"]', title)
    await page.evaluate('document.querySelector("form").submit()')
    await page.wait_for_url(f"{BASE_URL}/todos")


async def _get_todo_id(page, title: str = "Test todo"):
    """Get the todo ID from the list page."""
    link = page.locator(f'a[href^="/todos/"]:has-text("{title}")').first
    href = await link.get_attribute("href")
    return href.split("/")[-1]


async def test_empty_list(page):
    """The list page shows a placeholder when there are no todos."""
    await page.goto(f"{BASE_URL}/todos")
    assert "No todos found" in await _get_text(page)


async def test_list_shows_todo_rows(page):
    """The list page shows rows for pending todos."""
    await _create_todo(page, "Visible todo")
    await page.goto(f"{BASE_URL}/todos")
    assert "Visible todo" in await _get_text(page)


async def test_add_todo(page):
    """A user can add a new todo."""
    await _create_todo(page, "New todo")
    await page.goto(f"{BASE_URL}/todos")
    assert "New todo" in await _get_text(page)


async def test_add_todo_empty_title(page):
    """Adding a todo with an empty title shows an error."""
    await page.goto(f"{BASE_URL}/todos/add")
    await page.locator('input[name="title"]').fill("   ")
    await page.locator('button[type="submit"]').click()
    assert await page.locator('p.error').is_visible()


async def test_edit_todo(page):
    """A user can edit an existing todo."""
    await _create_todo(page, "Edit me")
    todo_id = await _get_todo_id(page, "Edit me")

    await page.goto(f"{BASE_URL}/todos/{todo_id}/edit")
    await page.fill('input[name="title"]', "Updated title")
    await page.evaluate('document.querySelector("form").submit()')
    await page.wait_for_url(f"{BASE_URL}/todos")
    assert "Updated title" in await _get_text(page)


async def test_edit_todo_empty_title(page):
    """Editing a todo with an empty title shows an error."""
    await _create_todo(page, "Edit me empty")
    todo_id = await _get_todo_id(page, "Edit me empty")

    await page.goto(f"{BASE_URL}/todos/{todo_id}/edit")
    await page.locator('input[name="title"]').fill("   ")
    await page.locator('button[type="submit"]').click()
    assert await page.locator('p.error').is_visible()


async def test_complete_todo(page):
    """A user can mark a todo as complete via HTMX."""
    await _create_todo(page, "Complete me")
    todo_id = await _get_todo_id(page, "Complete me")

    await page.goto(f"{BASE_URL}/todos")
    await page.click(f'tr#todo-{todo_id} button.btn-success')
    await page.wait_for_url(f"{BASE_URL}/todos")
    await page.wait_for_timeout(500)

    assert "✓" in await _get_text(page)
    assert "Complete me" in await _get_text(page)


async def test_complete_todo_redirect(page):
    """A user can mark a todo as complete via redirect (no HTMX)."""
    await _create_todo(page, "Complete redirect")
    todo_id = await _get_todo_id(page, "Complete redirect")

    await page.goto(f"{BASE_URL}/todos")
    await page.evaluate(f'document.querySelector("tr#todo-{todo_id} button.btn-success").click()')
    await page.wait_for_timeout(500)
    # Without HTMX, the browser follows the 302 redirect
    assert page.url.startswith(f"{BASE_URL}/todos")
    assert "Complete redirect" in await _get_text(page)


async def test_delete_todo(page):
    """A user can delete a todo via HTMX."""
    await _create_todo(page, "Delete me")
    todo_id = await _get_todo_id(page, "Delete me")

    await page.goto(f"{BASE_URL}/todos")
    await page.click(f'tr#todo-{todo_id} button.btn-danger')
    await page.wait_for_url(f"{BASE_URL}/todos")
    await page.wait_for_timeout(500)

    assert "No todos found" in await _get_text(page)


async def test_delete_todo_redirect(page):
    """A user can delete a todo via redirect (no HTMX)."""
    await _create_todo(page, "Delete redirect")
    todo_id = await _get_todo_id(page, "Delete redirect")

    await page.goto(f"{BASE_URL}/todos")
    await page.evaluate(f'document.querySelector("tr#todo-{todo_id} button.btn-danger").click()')
    await page.wait_for_timeout(500)
    assert page.url.startswith(f"{BASE_URL}/todos")
    assert "No todos found" in await _get_text(page)


async def test_show_todo(page):
    """A user can view todo details."""
    await _create_todo(page, "Show me")
    todo_id = await _get_todo_id(page, "Show me")

    await page.goto(f"{BASE_URL}/todos/{todo_id}")
    assert "Show me" in await _get_text(page)


async def test_show_todo_not_found(page):
    """Showing a non-existent todo returns 404."""
    await page.goto(f"{BASE_URL}/todos/nonexistent-id")
    assert "not found" in (await _get_text(page)).lower()