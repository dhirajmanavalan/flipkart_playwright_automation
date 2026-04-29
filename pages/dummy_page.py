from time import sleep
from playwright.sync_api import Page, Locator
import re
import tkinter as tk
from datetime import datetime

def get_screen_size():
    root = tk.Tk()
    root.withdraw()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return width, height

class ChartsVacancy:

        def __init__(self, context):
            self.context = context
            self.page = context.new_page()

        # LOCATORS
        CHART_BUTTON = "(//label[normalize-space()='CHARTS / VACANCY'])[1]"
        TRAIN_NUMBER = "(//input[contains(@id,'react-select')])[1]"
        BOARDING_STATION = "//div[text()='Boarding Station*']"
        BOARDING_STATION_INPUT = "//div[@id='boardingStation']//input[contains(@id,'react-select')]"
        TRAIN_CHART = "//span[normalize-space()='Get Train Chart']"

        URL = "https://www.irctc.co.in/"

        def load_page(self):
            # Open main page
            self.page.goto(self.URL)

            # Optional: dynamic screen size
            width, height = get_screen_size()
            self.page.set_viewport_size({"width": width, "height": height})

        def open_charts(self):
            # Click and capture new tab
            with self.context.expect_page() as new_page_info:
                self.page.locator(self.CHART_BUTTON).click()

            self.new_tab = new_page_info.value
            self.new_tab.wait_for_load_state()

            # Set full screen
            width, height = get_screen_size()
            self.new_tab.set_viewport_size({"width": width, "height": height})

            print("Charts Page Title:", self.new_tab.title())

        def select_train(self):
            train_input = self.new_tab.locator(self.TRAIN_NUMBER)
            train_input.wait_for(state="visible")

            # Step 3: Type train number
            train_input.type("12345", delay=100)
            train_input.press("Enter")
            sleep(5)

        def select_boarding_station(self):
            # Step 1: Click boarding station input
            self.new_tab.locator(self.BOARDING_STATION).click()
            boarding_input = self.new_tab.locator(self.BOARDING_STATION_INPUT)
            boarding_input.clear()
            boarding_input.fill("HWH")
            boarding_input.press("Enter")

            self.new_tab.locator(self.TRAIN_CHART).click()
            sleep(5)

class PNRStatus:
    def __init__(self, context):
        self.context = context
        self.page = context.new_page()

    URL = "https://www.irctc.co.in/"

    # LOCATORS
    PNR_BUTTON = "(//label[contains(@class,'search_btn') and normalize-space()='PNR STATUS'])[1]"
    PNR_NUMBER = "//input[@id='inputPnrNo']"
    SUBMIT_BUTTON = "//input[@id='modal1']"

    def load_page(self):
        width, height = get_screen_size()
        self.page.set_viewport_size({"width": width, "height": height})
        self.page.goto(PNRStatus.URL)

    def pnr_status(self):
        with self.context.expect_page() as new_page_info:
             self.page.locator(self.PNR_BUTTON).click()

        new_tab = new_page_info.value
        new_tab.wait_for_load_state()

        width, height = get_screen_size()
        new_tab.set_viewport_size({"width": width, "height": height})

        print(new_tab.title())

        pnr_number = new_tab.locator(self.PNR_NUMBER)
        pnr_number.fill("4136773029")

        new_tab.locator(self.SUBMIT_BUTTON).click()

class LoginPage:
    URL = "https://www.irctc.co.in/"

    def __init__(self, page:Page):
        self.page = page

    #LOCATORS
    LOGIN_REGISTER_BUTTON = "//a[text()=' LOGIN / REGISTER ']"
    USERNAME_INPUT_BOX = "//input[@placeholder='User Name']"
    PASSWORD_INPUT_BOX = "//input[@placeholder='Password']"
    SIGN_IN_BUTTON = "//button[text()='SIGN IN']"

    def load_page(self):
        width, height = get_screen_size()
        self.page.set_viewport_size({"width": width, "height": height})
        self.page.goto(LoginPage.URL)
        # self.page.set_viewport_size({"width": 1920, "height": 1080})

    def login(self):
        self.page.locator(self.LOGIN_REGISTER_BUTTON).click()

        username = self.page.locator(self.USERNAME_INPUT_BOX)
        password = self.page.locator(self.PASSWORD_INPUT_BOX)

        username.clear()
        username.fill("Dhiru_naughty")

        password.clear()
        password.fill("DhirDhir@12")

        self.page.click(self.SIGN_IN_BUTTON)

    def go_to_ticket_cancellation_history(self):
        # Step 1: Click MY ACCOUNT
        my_account = self.page.locator("//a[contains(.,'MY ACCOUNT')]")
        my_account.wait_for(state="visible")
        my_account.click()

        # Step 2: Hover My Transactions
        my_transactions = self.page.locator("//span[text()='My Transactions']")
        my_transactions.wait_for(state="visible")
        my_transactions.hover()

        # Step 3: Click Ticket Cancellation History
        cancellation = self.page.locator("//span[text()='Ticket Cancellation History']")
        cancellation.wait_for(state="visible")
        cancellation.click()

class SearchTrains:

    def __init__(self, page:Page):
        self.page = page

    # LOCATORS
    FROM_BOX = "//input[contains(@aria-label,'From station')]"
    TO_BOX = "//input[contains(@aria-label,'To station')]"
    DATE_BOX = "//span[contains(@class,'ui-calendar')]//input"
    CLASS_BOX = "//div[contains(@class,'ng-tns-c76-10 ui-dropdown')]"
    GENERAL_BOX = "//div[contains(@class,'ng-tns-c76-11 ui-dropdown')]"
    SEARCH_BUTTON = "//button[contains(@class,'search_btn')]"


    # HELPER METHODS
    def parse_date(self,date_str: str):
        # input: dd/mm/yyyy
        dt = datetime.strptime(date_str, "%d/%m/%Y")
        return dt.day, dt.strftime("%B"), dt.year

    def select_date_from_calendar(self, date: str):
        day, target_month, target_year = self.parse_date(date)

        # open calendar
        self.page.locator(self.DATE_BOX).click()

        while True:
            current_month = self.page.locator("//span[contains(@class,'ui-datepicker-month')]").inner_text()
            current_year = self.page.locator("//span[contains(@class,'ui-datepicker-year')]").inner_text()

            if current_month == target_month and int(current_year) == target_year:
                break

            # decide direction
            current_dt = datetime.strptime(f"{current_month} {current_year}", "%B %Y")
            target_dt = datetime.strptime(f"{target_month} {target_year}", "%B %Y")

            if current_dt < target_dt:
                # click next arrow
                self.page.locator("//a[contains(@class,'ui-datepicker-next')]").click()
            else:
                # click previous arrow
                self.page.locator("//a[contains(@class,'ui-datepicker-prev')]").click()

        # click day (avoid disabled dates)
        self.page.locator(f"//a[text()='{day}']").click()


    def search_trains(self, source:str, destination:str, date:str, classes:str, general:str):
        # FROM
        from_search = self.page.locator(self.FROM_BOX)
        from_search.fill(source)
        self.page.wait_for_timeout(1000)
        self.page.locator(f"//span[contains(.,'{source}')]")
        self.page.keyboard.press("Enter")

        # TO
        to_search = self.page.locator(self.TO_BOX)
        to_search.fill(destination)
        self.page.wait_for_timeout(1000)
        self.page.locator(f"//span[contains(.,'{destination}')]")
        self.page.keyboard.press("Enter")

        # DATE
        if date:
            self.select_date_from_calendar(date)

        #CLASSES
        self.page.locator(self.CLASS_BOX).click()
        self.page.wait_for_timeout(1000)
        self.page.locator(f"//li[@role='option' and contains(@aria-label,'{classes}')]").click()

        #GENERAL
        self.page.locator(self.GENERAL_BOX).click()
        self.page.wait_for_timeout(1000)
        self.page.locator(f"//li[@role='option' and contains(@aria-label,'{general}')]").click()

        #SEARCH
        self.page.wait_for_timeout(1000)
        self.page.locator(self.SEARCH_BUTTON).click()

class BookingPage:
    def __init__(self, page: Page):
        self.page = page

    TRAIN_CARDS = "xpath=//div[contains(@class,'form-group') and contains(@class,'bull-back') and contains(@class,'border-all')][.//app-train-avl-enq]"
    TRAIN_NAME = "xpath=.//div[contains(@class,'train-heading')]//strong"
    DIMMER = "css=div.dimmer"

    BOOK_NOW_ENABLED = "xpath=.//button[contains(@class,'btnDefault') and normalize-space()='Book Now' and not(contains(@class,'disable-book'))]"

    CONFIRMATION_POPUP = "xpath=//div[contains(@class,'ui-confirmdialog') and .//span[contains(normalize-space(),'Confirmation')]]"
    CONFIRMATION_YES_BUTTON = "xpath=//div[contains(@class,'ui-confirmdialog')]//button[.//span[normalize-space()='Yes']]"

    CLASS_MAP = {
        "SL": "xpath=.//div[contains(@class,'white-back') and contains(@class,'col-xs-12')]//td/div[contains(@class,'pre-avl')][.//strong[contains(normalize-space(),'Sleeper') and contains(normalize-space(),'SL')]]",
        "3A": "xpath=.//div[contains(@class,'white-back') and contains(@class,'col-xs-12')]//td/div[contains(@class,'pre-avl')][.//strong[contains(normalize-space(),'AC 3 Tier') and contains(normalize-space(),'3A')]]",
        "2A": "xpath=.//div[contains(@class,'white-back') and contains(@class,'col-xs-12')]//td/div[contains(@class,'pre-avl')][.//strong[contains(normalize-space(),'AC 2 Tier') and contains(normalize-space(),'2A')]]",
        "1A": "xpath=.//div[contains(@class,'white-back') and contains(@class,'col-xs-12')]//td/div[contains(@class,'pre-avl')][.//strong[contains(normalize-space(),'AC First Class') and contains(normalize-space(),'1A')]]",
        "3E": "xpath=.//div[contains(@class,'white-back') and contains(@class,'col-xs-12')]//td/div[contains(@class,'pre-avl')][.//strong[contains(normalize-space(),'AC 3 Economy') and contains(normalize-space(),'3E')]]",
        "CC": "xpath=.//div[contains(@class,'white-back') and contains(@class,'col-xs-12')]//td/div[contains(@class,'pre-avl')][.//strong[contains(normalize-space(),'Chair Car') and contains(normalize-space(),'CC')]]",
        "EC": "xpath=.//div[contains(@class,'white-back') and contains(@class,'col-xs-12')]//td/div[contains(@class,'pre-avl')][.//strong[contains(normalize-space(),'Exec. Chair Car') and contains(normalize-space(),'EC')]]",
        "2S": "xpath=.//div[contains(@class,'white-back') and contains(@class,'col-xs-12')]//td/div[contains(@class,'pre-avl')][.//strong[contains(normalize-space(),'Second Sitting') and contains(normalize-space(),'2S')]]",
    }

    def wait_for_results(self):
        try:
            self.page.wait_for_load_state("domcontentloaded")
        except Exception:
            pass

        self.page.locator(self.TRAIN_CARDS).first.wait_for(state="visible", timeout=30000)
        self.page.wait_for_timeout(2000)

    def _month_abbr(self, input_date: str) -> str:
        month_map = {
            "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
            "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
            "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
        }
        return month_map[input_date.split("/")[1]]

    def _day(self, input_date: str) -> str:
        return str(int(input_date.split("/")[0]))

    def _normalize(self, text: str) -> str:
        return re.sub(r"\s+", " ", text.strip()).upper()

    def _is_unavailable(self, status_text: str) -> bool:
        text = self._normalize(status_text)
        return (
            "TRAIN DEPARTED" in text
            or "NOT AVAILABLE" in text
            or "REGRET" in text
        )

    def _is_bookable(self, status_text: str) -> bool:
        return not self._is_unavailable(status_text)

    def _wait_for_dimmer_to_disappear(self):
        try:
            self.page.locator(self.DIMMER).wait_for(state="hidden", timeout=5000)
        except Exception:
            pass

    def _safe_click(self, locator: Locator, name: str):
        self._wait_for_dimmer_to_disappear()

        try:
            locator.scroll_into_view_if_needed(timeout=5000)
        except Exception:
            pass

        try:
            locator.wait_for(state="visible", timeout=10000)
            locator.click(timeout=10000)
            return
        except Exception as e:
            print(f"Normal click failed for {name}: {e}")

        self._wait_for_dimmer_to_disappear()

        try:
            locator.click(timeout=5000, force=True)
            return
        except Exception as e:
            print(f"Force click failed for {name}: {e}")

        self._wait_for_dimmer_to_disappear()

        try:
            locator.evaluate("element => element.click()")
            return
        except Exception as e:
            raise Exception(f"All click methods failed for {name}: {e}")

    def _get_date_block(self, train_card: Locator, day: str, month_abbr: str) -> Locator:
        return train_card.locator(
            f"xpath=.//td/div[contains(@class,'pre-avl')][.//strong[contains(normalize-space(),'{day}') and contains(normalize-space(),'{month_abbr}')]]"
        )

    def _get_status_from_date_block(self, date_block: Locator) -> str:
        strongs = date_block.locator("xpath=.//strong")
        count = strongs.count()

        if count >= 2:
            return strongs.nth(1).inner_text().strip()

        return strongs.first.inner_text().strip()

    def handle_confirmation_popup_if_present(self):
        try:
            popup = self.page.locator(self.CONFIRMATION_POPUP).first
            popup.wait_for(state="visible", timeout=3000)

            yes_button = self.page.locator(self.CONFIRMATION_YES_BUTTON).first
            yes_button.click()

            print(" Confirmation popup appeared, clicked Yes")
            self.page.wait_for_timeout(1500)

        except Exception:
            print("ℹ Confirmation popup did not appear, continuing normally")

    def select_train_based_on_availability(self, input_date: str, preferred_class: str = "SL"):
        self.wait_for_results()

        day = self._day(input_date)
        month_abbr = self._month_abbr(input_date)

        print(f"Looking for date: {day} {month_abbr}")

        train_cards = self.page.locator(self.TRAIN_CARDS)
        total_trains = train_cards.count()
        print(f"Total trains found: {total_trains}")

        for i in range(total_trains):
            try:
                train_card = train_cards.nth(i)

                try:
                    train_card.scroll_into_view_if_needed(timeout=5000)
                except Exception:
                    pass

                train_name = train_card.locator(self.TRAIN_NAME).first.inner_text().strip()
                print(f"Checking Train {i + 1}: {train_name}")

                class_locator = train_card.locator(self.CLASS_MAP[preferred_class])
                class_count = class_locator.count()

                if class_count == 0:
                    print(f"{preferred_class} class not found in {train_name}")
                    continue

                self._safe_click(class_locator.first, f"{preferred_class} class in {train_name}")
                self.page.wait_for_timeout(2000)

                date_block = self._get_date_block(train_card, day, month_abbr)
                date_count = date_block.count()

                if date_count == 0:
                    print(f"Date block not found for {input_date} in {train_name}")
                    continue

                status_text = self._get_status_from_date_block(date_block.first)
                print(f"Status on {input_date}: {status_text}")

                if self._is_unavailable(status_text):
                    print(f"No seats are available in {train_name}")
                    continue

                if self._is_bookable(status_text):
                    print(f"Seat is acceptable in {train_name}. Trying Book Now...")

                    self._safe_click(date_block.first, f"date block in {train_name}")
                    self.page.wait_for_timeout(1500)

                    book_now = train_card.locator(self.BOOK_NOW_ENABLED)
                    book_count = book_now.count()

                    if book_count >= 1:
                        self._safe_click(book_now.first, f"Book Now in {train_name}")
                        print(" Book Now clicked successfully")

                        self.handle_confirmation_popup_if_present()
                        return

                    print(f"Book Now button not enabled in {train_name}")
                    continue

            except Exception as e:
                print(f"Skipping train due to error: {e}")
                continue

        raise AssertionError("No valid train found for selected class and date")

class PassengerDetailsPage:
    def __init__(self, page: Page):
        self.page = page

    NAME_INPUTS = "xpath=//input[@role='searchbox' and @placeholder='Name']"
    AGE_INPUTS = "xpath=//input[@type='number' and @placeholder='Age']"
    GENDER_DROPDOWNS = "xpath=//select[@formcontrolname='passengerGender']"
    BERTH_DROPDOWNS = "xpath=//select[@formcontrolname='passengerBerthChoice']"
    ADD_PASSENGER_BUTTON = "xpath=//span[contains(@class,'prenext') and contains(normalize-space(),'+ Add Passenger')]"
    MOBILE_NUMBER_INPUT = "xpath=//input[@formcontrolname='mobileNumber' and @placeholder='Passenger mobile number *']"

    AUTO_UPGRADE_LABEL = (
        "xpath=//label[@for='autoUpgradation' and "
        "contains(normalize-space(),'Consider for Auto Upgradation')]"
    )

    # radio labels, not inputs
    PAYMENT_CARD_LABEL = (
        "xpath=//label[@for='3'and contains(normalize-space(),'Credit & Debit')]//div[@role='radio']"
    )
    PAYMENT_UPI_LABEL = (
        "xpath=//label[@for='2' and contains(normalize-space(),'BHIM/UPI')]//div[@role='radio']"
    )

    CONTINUE_BUTTON = (
        "xpath=//button[@type='submit' and contains(@class,'train_Search') "
        "and normalize-space()='Continue']"
    )

    def wait_for_passenger_page(self):
        self.page.locator(self.NAME_INPUTS).first.wait_for(state="visible", timeout=30000)
        self.page.wait_for_timeout(1000)

    def click_add_passenger(self):
        self.page.locator(self.ADD_PASSENGER_BUTTON).first.click()
        self.page.wait_for_timeout(1500)

    def fill_single_passenger(self, passenger_index: int, name: str, age: str, gender: str, berth: str):
        name_input = self.page.locator(self.NAME_INPUTS).nth(passenger_index)
        age_input = self.page.locator(self.AGE_INPUTS).nth(passenger_index)
        gender_dropdown = self.page.locator(self.GENDER_DROPDOWNS).nth(passenger_index)
        berth_dropdown = self.page.locator(self.BERTH_DROPDOWNS).nth(passenger_index)

        name_input.wait_for(state="visible", timeout=15000)

        name_input.click()
        name_input.fill(str(name))

        age_input.click()
        age_input.fill(str(age))

        gender_dropdown.select_option(value=str(gender).upper())
        berth_dropdown.select_option(value=str(berth).upper())

        self.page.wait_for_timeout(1000)

    def set_auto_upgrade(self, auto_upgrade: bool):
        if not auto_upgrade:
            print("Auto upgrade not requested, skipping")
            return

        try:
            label = self.page.locator(self.AUTO_UPGRADE_LABEL).first
            label.click(timeout=5000)
            print("Auto upgrade selected using label click")
            self.page.wait_for_timeout(1000)
        except Exception as e:
            print(f"Auto upgrade label not handled: {e}")

    def select_payment_mode(self, payment_mode: str):
        payment_mode = payment_mode.strip().lower()

        if payment_mode == "card":
            label = self.page.locator(self.PAYMENT_CARD_LABEL).first
        elif payment_mode == "upi":
            label = self.page.locator(self.PAYMENT_UPI_LABEL).first
        else:
            raise ValueError("payment_mode must be either 'card' or 'upi'")

        label.wait_for(state="visible", timeout=10000)
        label.click(timeout=5000)
        print(f"Payment mode selected via label: {payment_mode}")
        self.page.wait_for_timeout(1000)

    def click_continue(self):
        self.page.locator(self.CONTINUE_BUTTON).first.click()
        self.page.wait_for_timeout(2000)

    def fill_all_passengers(
        self,
        passengers: list[dict],
        mobile_number: str,
        auto_upgrade: bool = False,
        payment_mode: str = "card",
    ):
        self.wait_for_passenger_page()

        for index, passenger in enumerate(passengers):
            if index > 0:
                self.click_add_passenger()

            self.fill_single_passenger(
                passenger_index=index,
                name=passenger["name"],
                age=passenger["age"],
                gender=passenger["gender"],
                berth=passenger["berth"],
            )

        mobile_input = self.page.locator(self.MOBILE_NUMBER_INPUT).first
        mobile_input.click()
        mobile_input.fill(str(mobile_number))
        self.page.wait_for_timeout(1000)

        self.set_auto_upgrade(auto_upgrade)
        self.select_payment_mode(payment_mode)
        self.click_continue()

