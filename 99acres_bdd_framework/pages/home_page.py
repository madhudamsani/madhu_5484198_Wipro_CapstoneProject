from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import get_implicit_wait

import allure

from utilities.logger import LogGen
logger = LogGen.loggen()

class HomePage:
    """
    Page Object Model for 99acres Home Page.

    Handles:
    - Buy/Rent tab navigation
    - Property location search
    - Search submission
    - Dynamic stale element handling
    """

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            get_implicit_wait()
        )

    # =====================================================
    # LOCATORS
    # =====================================================

    # Buy Tab
    buy_tab = (
        By.ID,
        "inPageSearchForm_0"
    )

    # Rent Tab
    rent_tab = (
        By.ID,
        "inPageSearchForm_1"
    )

    # Rent Tab Alternative Locator
    rent_tab_by_text = (
        By.XPATH,
        "//*[not(ancestor::*[@data-label='SEARCH']) "
        "and normalize-space()='Rent']"
    )

    # Search Input
    search_box = (
        By.ID,
        "keyword2"
    )

    # Search Button
    search_button = (
        By.ID,
        "searchform_search_btn"
    )

    # Search Button Alternative Locator
    search_button_by_text = (
        By.XPATH,
        "//button[normalize-space()='Search']"
    )

    #searchbar with location
    displayed_location = (
        By.XPATH,
        "//*[@id='searchTabContainer']/div[1]/span[2]"

    )

    # =====================================================
    # COMMON METHODS
    # =====================================================

    def find_fresh_element(self, locators):
        """
        Find fresh visible element using
        single or multiple locators.

        Handles dynamic DOM refresh.
        """
        # Convert single locator to tuple
        if (
            isinstance(locators, tuple)
            and len(locators) == 2
            and isinstance(locators[0], str)
        ):

            locators = (locators,)

        last_error = None

        for locator in locators:

            try:

                return self.wait.until(
                    EC.visibility_of_element_located(
                        locator
                    )
                )

            except TimeoutException as error:

                last_error = error

        raise AssertionError(
            f"Unable to locate element "
            f"using locators: {locators}"
        ) from last_error

    def click_when_ready(self, locators):
        """
        Reusable safe click method.
        Features:
        - Handles stale elements
        - Handles dynamic UI refresh
        - Scrolls element into view
        - Uses JavaScript click
        """

        last_error = None

        for _ in range(5):

            try:

                element = self.find_fresh_element(
                    locators
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center'
                    });
                    """,
                    element
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    element
                )

                return

            except (
                StaleElementReferenceException,
                TimeoutException
            ) as error:

                last_error = error

        raise AssertionError(
            f"Unable to click element "
            f"using locators: {locators}"
        ) from last_error

    # =====================================================
    # ACTIONS
    # =====================================================

    def click_buy_tab(self):
        #Click Buy tab.
        self.click_when_ready(
            self.buy_tab
        )

    def click_rent_tab(self):
        """
        Click Rent tab using primary or fallback locator.
        """
        self.click_when_ready(
            (
                self.rent_tab,
                self.rent_tab_by_text
            )
        )

    def enter_location(self, location):
        """
        Enter property location in search field.
        Handles:
        - stale elements
        - dynamic DOM refresh
        """

        if not location:

            raise ValueError(
                "Location cannot be empty"
            )

        last_error = None

        for _ in range(5):

            try:

                search = self.wait.until(
                    EC.visibility_of_element_located(
                        self.search_box
                    )
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center'
                    });
                    """,
                    search
                )

                search.click()

                search.clear()

                search.send_keys(location)

                return

            except (
                StaleElementReferenceException,
                TimeoutException
            ) as error:

                last_error = error

                continue

        raise AssertionError(
            f"Unable to enter location: {location}"
        ) from last_error

    def click_search(self):
        #Click Search button using primary or fallback locator.

        self.click_when_ready(
            (
                self.search_button,
                self.search_button_by_text
            )
        )

    def get_displayed_location(self):

        location_element = self.wait.until(
            EC.visibility_of_element_located(
                self.displayed_location
            )
        )

        return (
            location_element.text.strip()
        )

    #screeshot method
    def capture_screenshot(self, screenshot_name):

        screenshot = (self.driver.get_screenshot_as_png())

        allure.attach(
            screenshot,
            name=screenshot_name,
            attachment_type=
            allure.attachment_type.PNG
        )

        logger.info(
            f"Screenshot Attached "
            f"To Allure Report: "
            f"{screenshot_name}"
        )
