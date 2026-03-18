from pages.base_page import BasePage


class SearchPage(BasePage):

    product_list = "//a[contains(@href,'/p/')]"

    def click_first_product(self):
        self.page.locator(self.product_list).first.wait_for()
        self.page.locator(self.product_list).first.click()

    def get_products(self):
        return self.page.locator(self.product_list).all_text_contents()