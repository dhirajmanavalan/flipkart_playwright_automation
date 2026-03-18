import pytest
from playwright.sync_api import sync_playwright
from cookies.cookie_config import CookieConfig

@pytest.fixture(scope="function")
def page():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        cookie_manager = CookieConfig(context)

        try:
            cookie_manager.load_cookie()
        except:
            print("Cookie file not found")

        page = context.new_page()

        page.goto("https://www.flipkart.com")

        yield page

        input()

        browser.close()