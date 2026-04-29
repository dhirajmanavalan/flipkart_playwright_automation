from time import sleep
import pytest
from pages.dummy_page import LoginPage, SearchTrains, BookingPage, PNRStatus, ChartsVacancy, PassengerDetailsPage

@pytest.mark.booking_irctc
def test_ticket_booking(page):
    passengers = [
        {"name": "DHIRAJKUMAR M", "age": "22", "gender": "M", "berth": "SL"},
        {"name": "DEV", "age": "22", "gender": "M", "berth": "SU"},
        {"name": "PARASHURAM", "age": "24", "gender": "M", "berth": "MB"},
        {"name": "VILAS", "age": "23", "gender": "M", "berth": "LB"},
        {"name": "MADHU", "age": "22", "gender": "F", "berth": "UB"},
    ]

    mobile_number = "8489403967"
    auto_upgrade = True
    payment_mode = "card"   # use "card" or "upi"

    login_page = LoginPage(page)
    login_page.load_page()
    login_page.login()

    page.wait_for_timeout(5000)

    search_trains = SearchTrains(page)
    search_trains.search_trains(
        source="MAS",
        destination="JTJ",
        date="30/04/2026",
        classes="SL",
        general="GENERAL",
    )

    page.wait_for_timeout(5000)

    booking_page = BookingPage(page)
    booking_page.select_train_based_on_availability(
        input_date="30/04/2026",
        preferred_class="SL"
    )

    passenger_page = PassengerDetailsPage(page)
    passenger_page.fill_all_passengers(
        passengers=passengers,
        mobile_number=mobile_number,
        auto_upgrade=auto_upgrade,
        payment_mode=payment_mode
    )
    sleep(13)

@pytest.mark.TICKET
def test_booking(page):
    login_page = LoginPage(page)
    login_page.load_page()
    login_page.login()

    page.wait_for_timeout(5000)

    search_trains = SearchTrains(page)
    search_trains.search_trains(
        source="HWH",
        destination="YPR",
        date="30/04/2026",
        classes="3A",
        general="GENERAL",
    )

    page.wait_for_timeout(5000)

    booking_page = BookingPage(page)
    booking_page.select_train_based_on_availability(
        input_date="30/04/2026",
        preferred_class="3A"
    )
    passenger_page = PassengerDetailsPage(page)
    passenger_page.fill_passenger_details(
        name="Parashuraman",
        age="24"
    )

    input("Enter space")
    sleep(3)

@pytest.mark.cancel
def test_cancel(page):
    login_page = LoginPage(page)
    login_page.load_page()
    login_page.login()

    page.wait_for_timeout(5000)
    login_page.go_to_ticket_cancellation_history()
    sleep(5)

@pytest.mark.login_irctc
def test_login(page):
    login_page = LoginPage(page)
    login_page.load_page()
    login_page.login()

    page.wait_for_timeout(3000)

    search_trains = SearchTrains(page)
    search_trains.search_trains(
        source="MAS",
        destination="TPT",
        date="30/04/2026",
        classes="SL",
        general="GENERAL",
    )
    sleep(5)

@pytest.mark.pnr
def test_pnr(page):
    pnr = PNRStatus(page)
    pnr.load_page()
    pnr.pnr_status()
    sleep(5)

@pytest.mark.chartvacancy
def test_charts(page):
    charts = ChartsVacancy(page)
    charts.load_page()
    charts.open_charts()
    charts.select_train()
    charts.select_boarding_station()
    sleep(5)







'''
from pages.dummy_page import LoginPage, SearchTrains, PNRStatus, ChartsVacancy, BookingPage
from time import sleep
import pytest

from time import sleep


@pytest.mark.booking
def test_ticket_booking(page):
    # Step 1: Login
    login_page = LoginPage(page)
    login_page.load_page()
    login_page.login()

    page.wait_for_timeout(5000)

    # Step 2: Search trains
    search_trains = SearchTrains(page=page)
    search_trains.search_trains(
        source="MAS",
        destination="TPT",
        date="29/04/2026",
        classes="SL",
        general="GENERAL",
    )

    # Wait for results
    page.wait_for_timeout(5000)


    # Step 3: Booking logic
    booking_page = BookingPage(page)
    booking_page.select_train_based_on_availability(input_date="29/04/2026")



@pytest.mark.cancel
def test_cancel(page):
    login_page = LoginPage(page)
    login_page.load_page()
    login_page.login()

    page.wait_for_timeout(5000)
    login_page.go_to_ticket_cancellation_history()
    sleep(5)

@pytest.mark.login
def test_login(page):
    login_page = LoginPage(page)
    login_page.load_page()
    login_page.login()

    page.wait_for_timeout(5000)

    search_trains = SearchTrains(page=page)
    search_trains.search_trains(source="MAS",destination="TPT",date="29/04/2026",classes="SL", general="LADIES")
    sleep(5)


@pytest.mark.pnr
def test_pnr(context):
    pnr = PNRStatus(context=context)
    pnr.load_page()
    pnr.pnr_status()
    sleep(5)

@pytest.mark.chartvacancy
def test_charts(context):
    charts = ChartsVacancy(context)

    charts.load_page()
    charts.open_charts()
    charts.select_train()
    charts.select_boarding_station()
    '''