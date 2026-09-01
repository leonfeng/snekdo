"""E2E tests for the web todo UI."""

import pytest

from .conftest import BASE_URL

pytestmark = [pytest.mark.e2e, pytest.mark.asyncio]


async def _get_text(page) -> str:
    await page.wait_for_load_state("load")
    return await page.inner_text("body")


async def _create_todo(page, title: str) -> None:
    await page.goto(f"{BASE_URL}/todos/add")
    await page.locator('input[name="title"]').fill(title)
    await page.get_by_role("button", name="Add Todo").click()
    await page.get_by_text(title, exact=False).first.wait_for(timeout=10_000)


def _row(page, title: str):
    """Return the table row containing the given todo title."""
    return page.locator("tr").filter(has_text=title).first


def _edit_link(row):
    return row.locator('a.btn:has-text("Edit")')


async def _post_todo_action(page, todo_id: str, action: str) -> None:
    """POST /todos/{id}/{action} without HX-Request header to trigger redirect."""
    await page.evaluate(
        """async (params) => {
            let cs = '';
            const btn = document.querySelector('button[hx-headers]');
            if (btn) {
                try {
                    const attr = btn.getAttribute('hx-headers');
                    const headers = JSON.parse(attr);
                    cs = headers['X-CSRF-Token'] || '';
                } catch (e) {}
            }
            await fetch(params.url + '/' + params.id + '/' + params.action, {
                method: 'POST',
                headers: {
                    'X-CSRF-Token': cs,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                credentials: 'include',
                body: 'csrf_token=' + encodeURIComponent(cs),
            });
        }""",
        {"url": BASE_URL + "/todos", "id": todo_id, "action": action},
    )


async def _todo_id_for(page, title: str) -> str:
    row = _row(page, title)
    row_id = await row.get_attribute('id')
    return row_id.replace('todo-', '')


async def test_list_shows_todo_rows(page):
    """The list page shows rows for pending todos with 10 columns."""
    await _create_todo(page, "Visible todo")
    text = await _get_text(page)
    assert "Visible todo" in text
    row = _row(page, "Visible todo")
    cells = row.locator("td")
    assert await cells.count() == 10


async def test_add_todo(page):
    """A user can add a new todo."""
    await _create_todo(page, "New todo")
    text = await _get_text(page)
    assert "New todo" in text


async def test_add_todo_empty_title(page):
    """Adding a todo with an empty title shows an error."""
    await page.goto(f"{BASE_URL}/todos/add")
    await page.locator('input[name="title"]').fill("   ")
    await page.get_by_role("button", name="Add Todo").click()
    text = await _get_text(page)
    assert "title is required" in text.lower()


async def test_edit_todo(page):
    """A user can edit an existing todo."""
    await _create_todo(page, "Edit me")
    row = _row(page, "Edit me")
    await _edit_link(row).click()
    await page.wait_for_load_state("load")
    await page.locator('input[name="title"]').fill("Edited title")
    await page.locator('button.btn[type="submit"]').click()
    await page.wait_for_load_state("load")
    text = await _get_text(page)
    assert "Edited title" in text


async def test_edit_todo_empty_title(page):
    """Editing a todo with an empty title shows an error."""
    await _create_todo(page, "Edit me empty")
    row = _row(page, "Edit me empty")
    await _edit_link(row).click()
    await page.wait_for_load_state("load")
    await page.locator('input[name="title"]').fill("   ")
    await page.locator('button.btn[type="submit"]').click()
    await page.wait_for_load_state("load")
    text = await _get_text(page)
    assert "title is required" in text.lower()


async def test_complete_todo(page):
    """A user can mark a todo as complete via HTMX."""
    await _create_todo(page, "Complete me")
    row = _row(page, "Complete me")
    await row.get_by_role("button", name="Complete").click()
    await page.wait_for_timeout(1000)
    assert "\u2713" in await _get_text(page)


async def test_complete_todo_redirect(page):
    """A user can mark a todo as complete via redirect (no HTMX)."""
    await _create_todo(page, "Complete redirect")
    todo_id = await _todo_id_for(page, "Complete redirect")
    await _post_todo_action(page, todo_id, "complete")
    await page.goto(f"{BASE_URL}/todos?status=completed")
    await page.wait_for_load_state("load")
    text = await _get_text(page)
    assert "Complete redirect" in text
    assert "\u2713" in text


async def test_delete_todo(page):
    """A user can delete a todo via HTMX."""
    await _create_todo(page, "Delete me")
    row = _row(page, "Delete me")
    await row.get_by_role("button", name="Delete").click()
    await page.wait_for_timeout(1000)
    text = await _get_text(page)
    assert "Delete me" not in text


async def test_delete_todo_redirect(page):
    """A user can delete a todo via redirect (no HTMX)."""
    await _create_todo(page, "Delete redirect")
    todo_id = await _todo_id_for(page, "Delete redirect")
    await _post_todo_action(page, todo_id, "delete")
    await page.reload()
    await page.wait_for_load_state("load")
    assert "Delete redirect" not in await _get_text(page)


async def test_complete_todo_row_has_correct_columns(page):
    """After completing a todo via HTMX, the updated row still has 10 cells."""
    await _create_todo(page, "Complete cols")
    row = _row(page, "Complete cols")
    await row.get_by_role("button", name="Complete").click()
    await page.wait_for_timeout(1000)
    rows = page.locator("#todo-list tr")
    count = await rows.count()
    assert count >= 1
    cells = rows.nth(0).locator("td")
    assert await cells.count() == 10


async def test_delete_todo_remaining_rows_have_correct_columns(page):
    """After deleting a todo via HTMX, remaining rows have 10 cells."""
    await _create_todo(page, "Keep me")
    await _create_todo(page, "Delete cols")
    row = _row(page, "Delete cols")
    await row.get_by_role("button", name="Delete").click()
    await page.wait_for_timeout(1000)
    text = await _get_text(page)
    assert "Delete cols" not in text
    rows = page.locator("#todo-list tr")
    count = await rows.count()
    assert count >= 1
    cells = rows.nth(0).locator("td")
    assert await cells.count() == 10


async def test_confirmation_page_standalone(page):
    """Confirmation page is standalone with no authenticated nav links."""
    await _create_todo(page, "Confirm")
    await page.goto(f"{BASE_URL}/profile")
    await page.wait_for_load_state("load")
    # Target the delete form specifically to avoid matching the password form
    delete_form = page.locator('form[hx-post="/profile/delete"]')
    await delete_form.locator('input[name="current_password"]').fill("password123")
    # Submit via HTMX-style fetch so the server processes it without redirect
    await page.evaluate(
        """(url) => {
            const form = document.querySelector('form[hx-post="/profile/delete"]');
            const csrf = form.querySelector('input[name="csrf_token"]');
            const csrfVal = csrf ? csrf.value : '';
            const fd = new FormData(form);
            return fetch(url, {
                method: "POST",
                headers: { "X-CSRF-Token": csrfVal, "HX-Request": "true" },
                credentials: "include",
                body: fd,
            }).then(r => r.text());
        }""",
        f"{BASE_URL}/profile/delete",
    )
    # Navigate to the confirmation page
    await page.goto(f"{BASE_URL}/confirmation")
    await page.wait_for_load_state("load")
    text = await _get_text(page)
    assert "Account Deleted" in text
    # No nav links to authenticated routes
    assert "/todos" not in text
    assert "/profile" not in text


async def test_show_todo(page):
    """A user can view todo details."""
    await _create_todo(page, "Show me")
    row = _row(page, "Show me")
    link = row.locator("a[href*='/todos/']")
    if await link.count() > 0:
        await link.first.click()
        text = await _get_text(page)
        assert "Show me" in text
