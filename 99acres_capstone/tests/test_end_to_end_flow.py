import time
import allure
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.property_details_page import PropertyDetailsPage
from pages.search_results_page import SearchResultsPage
from pages.filters_page import FiltersPage
from utilities.logger import LogGen
from utilities.excel_reader import get_test_data


logger = LogGen.loggen()

data = get_test_data()


@allure.feature(
    "99acres Rent Module"
)
@allure.story(
    "End-to-End Property Search"
)
@allure.severity(
    allure.severity_level.CRITICAL
)
@allure.description(
    "Validate complete end-to-end "
    "property search flow including "
    "login, filters, sorting, "
    "property details and owner contact."
)
def test_end_to_end_property_flow(driver):

    # =====================================================
    # LOGIN FLOW
    # =====================================================

    with allure.step(
        "Login Into 99acres"
    ):

        login = LoginPage(driver)

        logger.info(
            "Hovering Profile Icon"
        )

        login.hover_profile_icon()

        logger.info(
            "Clicking Login/Register"
        )

        login.click_login_register()

        logger.info(
            "Entering Mobile Number"
        )

        login.enter_mobile_number(
            data["mobile_number"]
        )

        logger.info(
            "Clicking Continue"
        )

        login.click_continue()

        logger.info(
            "Waiting 25 seconds "
            "for manual OTP entry"
        )

        time.sleep(25)

        logger.info(
            "Clicking Verify & Continue"
        )

        login.click_verify_and_continue()

        logger.info(
            "Login Successful"
        )

        login.wait_for_overlay_to_disappear()

    # =====================================================
    # HOME PAGE FLOW
    # =====================================================

    with allure.step(
        "Search Rental Property"
    ):

        home = HomePage(driver)

        logger.info(
            "Clicking Rent Tab"
        )

        home.click_rent_tab()

        logger.info(
            f"Entering Location: "
            f"{data['location']}"
        )

        home.enter_location(
            data["location"]
        )

        logger.info(
            "Clicking Search Button"
        )

        home.click_search()

    # =====================================================
    # SEARCH RESULTS VALIDATION
    # =====================================================

    results_page = SearchResultsPage(
        driver
    )

    with allure.step(
        "Verify Search Results Page"
    ):

        assert (
            results_page.verify_search_results()
        )

    logger.info(
        f"Results Heading: "
        f"{results_page.get_results_heading()}"
    )

    initial_results_count = (
        results_page.get_results_count()
    )

    logger.info(
        f"Initial Results Count: "
        f"{initial_results_count}"
    )

    # =====================================================
    # FILTER FLOW
    # =====================================================

    filters = FiltersPage(driver)

    logger.info(
        "Handling Blocking Popups"
    )

    filters.click_ok_understood()

    # -----------------------------------------------------

    with allure.step(
        "Apply 2 BHK Filter"
    ):

        logger.info(
            "Applying 2 BHK Filter"
        )

        filters.apply_2_bhk_filter()

        assert (
            filters.is_applied_filter_present(
                "2 BHK"
            )
        )

    # -----------------------------------------------------

    with allure.step(
        "Apply Flat/Apartment Filter"
    ):

        logger.info(
            "Applying Flat/Apartment Filter"
        )

        filters.apply_flat_apartment_filter()

        assert (
            filters.is_applied_filter_present(
                "Flat/Apartment"
            )
        )

    # -----------------------------------------------------

    with allure.step(
        "Apply Owner Filter"
    ):

        logger.info(
            "Applying Owner Filter"
        )

        filters.apply_owner_filter()

        assert (
            filters.is_applied_filter_present(
                "Owner"
            )
        )

    # -----------------------------------------------------

    with allure.step(
        "Apply Single Men Filter"
    ):

        logger.info(
            "Applying Single Men Filter"
        )

        filters.apply_single_men_filter()

        assert (
            filters.is_applied_filter_present(
                "Single Men"
            )
        )

    # -----------------------------------------------------

    with allure.step(
        "Sort Results By Price Low To High"
    ):

        logger.info(
            "Applying Sort: "
            "Price Low To High"
        )

        filters.sort_price_low_to_high()

    # -----------------------------------------------------

    with allure.step(
        "Verify All Required Filters Applied"
    ):

        assert (
            filters.verify_required_filters_applied()
        )

    # =====================================================
    # FILTERED RESULTS VALIDATION
    # =====================================================

    with allure.step(
        "Verify Filtered Results"
    ):

        logger.info(
            "Verifying Filtered Results"
        )

        assert (
            filters.verify_filtered_results()
        )

    filtered_results_count = (
        filters.get_results_count()
    )

    logger.info(
        f"Filtered Results Count: "
        f"{filtered_results_count}"
    )

    # =====================================================
    # OPEN PROPERTY DETAILS PAGE
    # =====================================================

    with allure.step(
        "Open First Filtered Property"
    ):

        logger.info(
            "Selecting First "
            "Filtered Property"
        )

        assert (
            filters.select_first_result()
        )

    # =====================================================
    # PROPERTY DETAILS PAGE
    # =====================================================

    property_page = PropertyDetailsPage(
        driver
    )

    with allure.step(
        "Switch To Property Window"
    ):

        logger.info(
            "Switching To Property Window"
        )

        property_page.switch_to_property_window()

    property_page.handle_blocking_popups()

    # -----------------------------------------------------

    with allure.step(
        "Shortlist Property"
    ):

        logger.info(
            "Clicking Shortlist Button"
        )

        property_page.click_shortlist()

    property_page.handle_blocking_popups()

    # -----------------------------------------------------

    with allure.step(
        "Open Owner Details"
    ):

        logger.info(
            "Opening Owner Details Section"
        )

        property_page.open_owner_details()

    property_page.handle_blocking_popups()

    # -----------------------------------------------------

    with allure.step(
        "View Owner Phone Number"
    ):

        logger.info(
            "Clicking View Phone Number"
        )

        property_page.click_view_phone_number()

    # -----------------------------------------------------

    with allure.step(
        "Verify Contact Section"
    ):

        logger.info(
            "Verifying Contact Section"
        )

        assert (
            property_page.verify_contact_section()
        )

    # =====================================================
    # PROPERTY VALIDATIONS
    # =====================================================

    with allure.step(
        "Get Property Details"
    ):

        property_title = (
            property_page.get_property_title()
        )

        rent_amount = (
            property_page.get_rent_amount()
        )

        logger.info(
            f"Property Title: "
            f"{property_title[:150]}"
        )

        logger.info(
            f"Rent Amount: "
            f"{rent_amount}"
        )

    logger.info(
        "End-to-End Property Flow "
        "Completed Successfully"
    )