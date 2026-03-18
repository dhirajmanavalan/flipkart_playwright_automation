from pages.base_page import BasePage

class HomePage(BasePage):

    travel_icon = "//a[contains(@href,'flights-travel')]"
    search_box = "(//input[@placeholder='Search for Products, Brands and More'])[1]"
    Mytrip = "(//img[@alt='Image'])[8]"
    plan_trip = "(//a[normalize-space()='PLAN A TRIP'])[1]"

    def click_travel_icon(self):
        self.click(self.travel_icon)


    def click_my_trip(self):
        self.click(self.Mytrip)


    def search_product(self, product_name):
        self.type(self.search_box, product_name)
        self.press_key("Enter")

    def plan_my_trip(self):
        self.click(self.plan_trip)
