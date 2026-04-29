import pickle
from playwright.sync_api import sync_playwright

COOKIE_PATH = r"C:\Users\dhira\flipkart_playwright_automation\cookies\flipkart_cookies.pkl"

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.flipkart.com")

    print("Login manually and enter OTP")

    input("After login press ENTER here...")

    cookies = context.cookies()

    with open(COOKIE_PATH, "wb") as file:
        pickle.dump(cookies, file)

    print("Cookies saved successfully")

    browser.close()