from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.cart_page import CartPage
import pytest

@pytest.mark.addtocart
def test_add_to_cart(page):
    home_page = HomePage(page)
    # Search for a product
    home_page.search_product("laptop")
    
    search_page = SearchPage(page)
    
    # Click on the first product; this typically opens in a new tab on Flipkart
    with page.expect_popup() as new_page_info:
        search_page.click_first_product()
        
    new_page = new_page_info.value
    new_page.wait_for_load_state()
    
    # Switch to the cart page with the newly opened tab
    cart_page = CartPage(new_page)
    cart_page.add_to_cart()
    
    # Wait to visually observe the item added to the cart
    new_page.wait_for_timeout(5000)
    
    # Optionally, we can verify the cart contents or successful addition message here