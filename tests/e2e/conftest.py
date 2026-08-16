"""E2E test fixtures for the snekdo web frontend.

Provides a running test server (uvicorn in a background thread) and a
Playwright browser page for each E2E test.
"""

import asyncio
import threading
import time

import pytest
import uvicorn
from playwright.async_api import async_playwright

from snekdo.api import create_app
from snekdo.web import get_template_env, register_web_routes

# Module-level base URL for E2E tests (set by the page fixture)
BASE_URL = "http://127.0.0.1:8765"


@pytest.fixture
def e2e_server(tmp_path):
    """Start a test server and yield the base URL.

    Creates a temporary FastAPI app with web routes and starts a uvicorn
    server on a fixed port.
    """
    storage_file = tmp_path / "todos.json"
    app = create_app(storage_path=str(storage_file))
    app.state.template_env = get_template_env()
    app.state.storage_path = str(storage_file)
    register_web_routes(app, storage_path=str(storage_file))

    port = 8765
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=port,
        log_level="warning",
        reload=False,
        access_log=False,
    )
    server = uvicorn.Server(config)

    def run_server():
        asyncio.run(server.serve())

    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    time.sleep(0.5)  # Wait for the server to bind and start

    yield f"http://127.0.0.1:{port}"

    server.should_exit = True
    thread.join(timeout=5)


@pytest.fixture
async def page(e2e_server):
    """Provide a Playwright page for E2E tests.

    Registers and logs in a test user so all protected routes are accessible.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        global BASE_URL
        BASE_URL = e2e_server
        base = e2e_server
        # Register a test user
        await page.goto(f"{base}/auth/register")
        await page.fill('input[name="username"]', "testuser")
        await page.fill('input[name="password"]', "password123")
        await page.click('button[type="submit"]')
        await page.wait_for_url(f"{base}/auth/login")

        # Log in the test user
        await page.goto(f"{base}/auth/login")
        await page.fill('input[name="username"]', "testuser")
        await page.fill('input[name="password"]', "password123")
        await page.click('button[type="submit"]')
        await page.wait_for_url(base)

        yield page
        await context.close()
        await browser.close()
