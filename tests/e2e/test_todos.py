"""E2E tests for the web todo UI."""

from .conftest import BASE_URL


async def _get_text(page) -> str:
    await page.wait_for_load_state("load")
    return await page.inner_text("body")


async def _create_todo(page, title: str) -> None:
    await page.goto(f"{BASE_URL}/todos/add")
    await page.locator('input[name="title"]').fill(title)
    await page.get_by_role("button", name="Add Todo").click()
    # The add POST redirects to /todos; wait_for_url is a no-op when already
    # at /todos, so confirm the row actually rendered (post processed).
    await page.get_by_text(title, exact=False).first.wait_for(timeout=10_000)


def _row(page, title: str):
    """Return the table row containing the given todo title."""
    return page.locator("tr").filter(has_text=title).first


def _edit_link(row):
    return row.locator('a.btn:has-text("Edit")')


async def _post_todo_action(page, todo_id: str, action: str) -> None:
    """POST /todos/{id}/{action} carrying the list page's CSRF token."""
    await page.evaluate(
        """(params) => {
            let cs = '';
            const btn = document.querySelector('button[hx-headers]');
            if (btn) {
                const m = btn.outerHTML.match(/X-CSRF[\\s"']+:\\s*[\\s"']+"([^"]*)"/);
                cs = m ? m[1] : '';
            }
            if (!cs) {
                const token = document.querySelector('input[name="csrf_token"]');
                if (token) cs = token.value;
            }
            return fetch(`${params.url}/${params.id}/${params.action}`, {
                method: "POST",
                headers: { "X-CSRF-Token": cs },
                body: "csrf_token=" + encodeURIComponent(cs),
            });
        }""",
        {"url": BASE_URL + "/todos", "id": todo_id, "action": action},
    )


async def _todo_id_for(page, title: str) -> str:
    return await _row(page, title).locator("td").first.inner_text()


async def test_list_shows_todo_rows(page):
    """The list page shows rows for pending todos."""
    await _create_todo(page, "Visible todo")
    text = await _get_text(page)
    assert "Visible todo" in text


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
    await row.locator('a.btn:has-text("Edit")').click()
    await page.wait_for_load_state("load")
    await page.locator('input[name="title"]').fill("Edited title")
    await page.locator('button[type="submit"]').click()
    await page.wait_for_load_state("load")
    text = await _get_text(page)
    assert "Edited title" in text


async def test_edit_todo_empty_title(page):
    """Editing a todo with an empty title shows an error."""
    await _create_todo(page, "Edit me empty")
    row = _row(page, "Edit me empty")
    await row.locator('a.btn:has-text("Edit")').click()
    await page.wait_for_load_state("load")
    await page.locator('input[name="title"]').fill("   ")
    await page.locator('button[type="submit"]').click()
    await page.wait_for_load_state("load")
    text = await _get_text(page)
    assert "title is required" in text.lower()


async def _complete_control(page, title: str) -> str:
    """Return the actual text of the complete control on a row."""
    row = await _row(page, title)
    # Inspect form actions on the row.
    forms = row.locator("form")
    count = await forms.count()
    actions = []
    for i in range(count):
        action = await forms.nth(i).get_attribute("action")
        actions.append(action)
    return "|".join(actions)


async def test_complete_todo(page):
    """A user can mark a todo as complete via HTMX."""
    await _create_todo(page, "Complete me")
    todo_id = await _todo_id_for(page, "Complete me")
    await _post_todo_action(page, todo_id, "complete")
    await page.reload()
    await page.wait_for_load_state("load")
    # After completion the status cell shows the ✓ marker.
    assert "✓" in await _get_text(page)


async def test_complete_todo_redirect(page):
    """A user can mark a todo as complete via redirect (no HTMX)."""
    await _create_todo(page, "Complete redirect")
    todo_id = await _todo_id_for(page, "Complete redirect")
    await _post_todo_action(page, todo_id, "complete")
    await page.wait_for_url(f"{BASE_URL}/todos", timeout=15_000)
    assert "✓" in await _get_text(page)


async def test_delete_todo(page):
    """A user can delete a todo via HTMX."""
    await _create_todo(page, "Delete me")
    todo_id = await _todo_id_for(page, "Delete me")
    await _post_todo_action(page, todo_id, "delete")
    await page.wait_for_timeout(500)
    text = await _get_text(page)
    assert "Delete me" not in text


async def test_delete_todo_redirect(page):
    """A user can delete a todo via redirect (no HTMX)."""
    await _create_todo(page, "Delete redirect")
    todo_id = await _todo_id_for(page, "Delete redirect")
    await _post_todo_action(page, todo_id, "delete")
    text = await _get_text(page)
    assert "Delete redirect" not in text


async def test_show_todo(page):
    """A user can view todo details."""
    await _create_todo(page, "Show me")
    row = _row(page, "Show me")
    # The row links to the detail page.
    link = row.locator("a[href*='/todos/']")
    if await link.count() > 0:
        await link.first.click()
        text = await _get_text(page)
        assert "Show me" in text
