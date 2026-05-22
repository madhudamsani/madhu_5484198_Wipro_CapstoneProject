import re

from selenium.webdriver.common.by import By

from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException
)

from selenium.webdriver.support.ui import (
    WebDriverWait
)

from selenium.webdriver.support import (
    expected_conditions as EC
)

from config.config import (
    get_implicit_wait
)


class SearchResultsPage:
    """
    Page Object Model for 99acres Search Results Page.

    Handles:
    - Search results validation
    - Results heading extraction
    - Property results count extraction
    - Dynamic results handling
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

    # Results Heading
    results_heading = (
        By.TAG_NAME,
        "h1"
    )

    # Property Cards
    property_cards = (
        By.CSS_SELECTOR,
        "div[data-label='SEARCH']"
    )

    # Result Count Text
    result_count_text = (
        By.XPATH,
        "//*[contains("
        "translate("
        "normalize-space(),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'"
        "),"
        "'results')]"
    )

    # =====================================================
    # PAGE VALIDATION
    # =====================================================

    def wait_for_results_page(self):
        """
        Wait for search results page
        to load successfully.
        """

        try:

            self.wait.until(
                EC.url_contains("property")
            )

        except TimeoutException as error:

            raise AssertionError(
                "Search results page "
                "did not load successfully"
            ) from error

    def verify_search_results(self):
        """
        Verify results heading
        is visible and valid.
        """

        self.wait_for_results_page()

        try:

            heading = self.wait.until(
                EC.visibility_of_element_located(
                    self.results_heading
                )
            )

            return (
                heading.is_displayed()
                and heading.text.strip() != ""
            )

        except TimeoutException as error:

            raise AssertionError(
                "Search results heading "
                "not visible"
            ) from error

    # =====================================================
    # RESULTS HEADING
    # =====================================================

    def get_results_heading(self):
        """
        Fetch visible results heading.
        """

        try:

            heading = self.wait.until(
                EC.visibility_of_element_located(
                    self.results_heading
                )
            )

            return heading.text.strip()

        except TimeoutException as error:

            raise AssertionError(
                "Unable to fetch "
                "results heading"
            ) from error

    # =====================================================
    # RESULTS COUNT
    # =====================================================

    def get_results_count(self):
        """
        Get total property results count.

        Strategy:
        1. Try extracting visible count text
        2. Fallback to counting property cards
        """

        count = (
            self.get_results_count_from_visible_text()
        )

        if count is not None:

            return count

        results = self.driver.find_elements(
            *self.property_cards
        )

        return len(results)

    def get_results_count_from_visible_text(self):
        """
        Extract results count
        from visible page text.
        """

        try:

            return WebDriverWait(
                self.driver,
                10
            ).until(
                lambda driver:
                self.extract_results_count()
            )

        except TimeoutException:

            return None

    def extract_results_count(self):
        """
        Extract numerical results count
        using regex matching.
        """

        candidates = [
            self.get_results_heading()
        ]

        elements = self.driver.find_elements(
            *self.result_count_text
        )

        for element in elements:

            try:

                if element.is_displayed():

                    candidates.append(
                        element.text
                    )

            except (
                StaleElementReferenceException,
                TimeoutException
            ):

                continue

        for text in candidates:

            match = re.search(
                r"([\d,]+)\s+results?",
                text,
                re.IGNORECASE
            )

            if match:

                return int(
                    match.group(1).replace(",", "")
                )

        return 0
