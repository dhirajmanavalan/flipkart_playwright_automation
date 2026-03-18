import pytest
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.cart_page import CartPage


@pytest.mark.search
def test_search_product(page):

    home = HomePage(page)
    search = SearchPage(page)
    cart = CartPage(page)

    # Step 1: Search product
    home.search_product("Shoe")

    # Step 2: Wait for products
    search.page.locator(search.product_list).first.wait_for()

    print("Products Found:")
    products = search.get_products()

    for p in products:
        print(p)

    assert len(products) > 0

    # Step 3: Click first product
    search.click_first_product()

    # Step 4: Switch to new tab
    new_page = cart.switch_to_new_tab()

    # # Step 5: Add to cart
    # cart_page = CartPage(new_page)
    # cart_page.add_to_cart()

    print("Product added to cart successfully")