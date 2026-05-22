import pytest
import allure

from selenium.webdriver.common.by import By
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.filters_page import FiltersPage
from pages.property_details_page import PropertyDetailsPage
from utilities.excel_reader import get_test_data
from utilities.logger import LogGen

logger = LogGen.loggen()

data = get_test_data()

@allure.feature("99acres Property Flows")
@pytest.mark.usefixtures("driver")
class TestCases:

    #common search flow
    def perform_search(self,driver,location):

        with allure.step("Search Rental Property"):

            logger.info("Starting Search Flow")
            home = HomePage(driver)
            logger.info("Clicking Rent Tab")
            home.click_rent_tab()
            logger.info(f"Entering Location: {location}")
            home.enter_location(location)
            logger.info("Clicking Search")
            home.click_search()
        results_page = SearchResultsPage(driver)

        with allure.step("Verify Search Results"):
            assert (results_page.verify_search_results())

        filters = FiltersPage(driver)
        logger.info("Closing Result Page Popups" )
        filters.click_ok_understood()
        return results_page

    # =====================================================
    # POSITIVE TEST CASE 1
    # =====================================================

    @allure.title("Positive 1:Verify Valid Property Search")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_property_search(self,driver):

        results_page = (self.perform_search(driver,data["location"]))
        home = HomePage(driver)
        with allure.step("Verify Results Heading"):

            heading = (results_page.get_results_heading())
            logger.info(f"Results Heading: {heading}")
            assert "rent" in heading.lower()
        home.capture_screenshot("valid_property_search")

    # =====================================================
    # POSITIVE TEST CASE 2
    # =====================================================

    @allure.title("Positive 2:Verify 2 BHK Filter")
    @allure.severity(allure.severity_level.NORMAL)
    def test_apply_2bhk_filter(self,driver):
        home = HomePage(driver)
        self.perform_search(driver, data["location"])
        filters = FiltersPage(driver)

        with allure.step("Apply 2 BHK Filter"):

            filters.apply_2_bhk_filter()
            assert filters.verify_filtered_results()
            #assert (filters.get_bhk_text() == "2 BHK")

        home.capture_screenshot("2bhk_filter")

    # =====================================================
    # POSITIVE TEST CASE 3
    # =====================================================

    @allure.title("Positive 3: Verify Searched Location Is Displayed In Search Bar")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_location_displayed(self, driver):

        home = HomePage(driver)
        self.perform_search(driver, data["location"])
        logger.info("Getting Displayed Location" )
        displayed_location = home.get_displayed_location()
        logger.info(f"Displayed Location: {displayed_location} ")
        expected_location = (data["location"].lower().replace("rent in", "").strip())
        assert (displayed_location.lower()== expected_location)
        home.capture_screenshot("search_location_displayed")

    # =====================================================
    # POSITIVE TEST CASE 4
    # =====================================================

    @allure.title("Positive 4: Verify Property Details Page")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_property_details_page(self, driver):
        home = HomePage(driver)
        self.perform_search(driver, data["location"])
        filters = FiltersPage(driver)

        with allure.step( "Open First Property"):

            filters.select_first_result()

        property_page = (PropertyDetailsPage(driver))

        with allure.step("Switch To Property Window"):

            property_page.switch_to_property_window()

        property_page.handle_blocking_popups()

        with allure.step("Get Property Details"):

            title = (property_page.get_property_title())
            rent = (property_page.get_rent_amount())
            logger.info(f"Property Title: {title[:150]}")
            logger.info(f"Rent Amount: {rent}")

        home.capture_screenshot("property_details_page")

        assert (title is not None and len(title) > 0)
        assert (rent is not None and len(rent) > 0)

    # =====================================================
    # NEGATIVE TEST CASE 1
    # =====================================================

    @allure.title("Negative 1:Verify Shortlist Requires Login")
    @allure.severity(allure.severity_level.NORMAL)
    def test_shortlist_requires_login(self, driver):
        home = HomePage(driver)
        self.perform_search(driver, data["location"])
        filters = FiltersPage(driver)

        with allure.step("Apply 2 BHK Filter"):

            filters.apply_2_bhk_filter()
            assert (filters.verify_filtered_results())

        with allure.step("Apply Owner Filter"):

            logger.info("Applying Owner Filter")
            filters.apply_owner_filter()
            assert (filters.is_applied_filter_present("Owner"))

        with allure.step("Open First Property"):

            filters.select_first_result()

        property_page = (PropertyDetailsPage(driver))

        with allure.step("Switch To Property Window"):

            property_page.switch_to_property_window()

        property_page.handle_blocking_popups()

        with allure.step("Click Shortlist Button"):
            property_page.click_shortlist()

        with allure.step("Verify Login Popup Appears"):

            assert property_page.is_login_popup_displayed()

        home.capture_screenshot("shortlist_login_popup")

    # =====================================================
    # NEGATIVE TEST CASE 2
    # =====================================================

    @allure.title("Verify Empty Location Validation")
    @allure.severity(allure.severity_level.MINOR)
    def test_empty_location_search_validation(self, driver):
        home = HomePage(driver)

        with allure.step("Click Rent Tab"):
            home.click_rent_tab()

        initial_url = driver.current_url

        with allure.step("Click Search Without Location"):
            home.click_search()

        with allure.step("Verify Search Results Page Is Not Opened"):

            current_url = driver.current_url
            logger.info(f"Initial URL: {initial_url}")
            logger.info(f"Current URL: {current_url}")
            assert current_url == initial_url

        home.capture_screenshot("empty_location_validation")