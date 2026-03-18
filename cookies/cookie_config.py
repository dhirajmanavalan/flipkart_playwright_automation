import pickle

class CookieConfig:

    def __init__(self, context):
        self.context = context

    def load_cookie(self):

        COOKIE_PATH = r"C:\Users\dhira\PycharmProjects\Flipkart_Playwright_Automation\cookies\flipkart_cookies.pkl"

        cookies = pickle.load(open(COOKIE_PATH, "rb"))

        self.context.add_cookies(cookies)

        print("Logged in with Cookies")