from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://the-internet.herokuapp.com/login")
    page.fill("#username","tomsmith")

    page.fill("#password", "SuperSecretPassword!")

    page.click("button[type='submit']")

    input()
    browser.close()