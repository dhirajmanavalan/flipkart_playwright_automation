from pages.base_page import BasePage


class CartPage(BasePage):

    add_to_cart_btn = "text=Add to cart"

    def switch_to_new_tab(self):
        pages = self.page.context.pages
        return pages[-1]

    def add_to_cart(self):
        self.page.locator(self.add_to_cart_btn).wait_for()
        self.page.locator(self.add_to_cart_btn).click()