from pages.home_page import HomePage
import pytest

@pytest.mark.travel
def test_open_travel(page):

    home = HomePage(page)
    home.click_travel_icon()
    page.wait_for_timeout(3000)

@pytest.mark.mytrips
def test_click_my_trips(page):

    home = HomePage(page)
    home.click_my_trip()
    page.wait_for_timeout(3000)

@pytest.mark.plantrip
def test_plan_my_trip(page):

    home = HomePage(page)
    home.plan_my_trip()
    page.wait_for_timeout(3000)