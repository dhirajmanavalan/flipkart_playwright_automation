import pytest

@pytest.mark.login
def test_login(page):

    page.wait_for_timeout(5000)

    print("Flipkart opened with saved cookies")