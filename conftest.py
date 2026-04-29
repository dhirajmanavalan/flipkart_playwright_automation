import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="function")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page

@pytest.fixture(scope="function")
def mobile_page():
    with sync_playwright() as p:
        iphone_12 = p.devices['iPhone 12']
        browser = p.chromium.launch(headless=False)
        # Apply the pre-configured device profile
        context = browser.new_context(**iphone_12)
        page = context.new_page()

        yield page

        context.close()
        browser.close()










# import pytest
# from playwright.sync_api import sync_playwright
# from cookies.cookie_config import CookieConfig
#
# @pytest.fixture(scope="function")
# def page():
#     p =  sync_playwright().start()
#     browser = p.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#
#     yield page
#
#     context.close()
#     browser.close()
#
#
#
# @pytest.fixture(scope="function")
# def context():
#     p =  sync_playwright().start()
#     browser = p.chromium.launch(headless=False)
#     context = browser.new_context()
#
#     yield context
#
#     context.close()
#     browser.close()
