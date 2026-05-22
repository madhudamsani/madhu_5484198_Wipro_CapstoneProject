import time

import allure
from behave import then, when

from pages.filters_page import FiltersPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.property_details_page import PropertyDetailsPage
from pages.search_results_page import SearchResultsPage
from utilities.logger import LogGen


logger = LogGen.loggen()


def home_page(context):
    if not hasattr(context, "home_page"):
        context.home_page = HomePage(context.driver)
    return context.home_page


def login_page(context):
    if not hasattr(context, "login_page"):
        context.login_page = LoginPage(context.driver)
    return context.login_page


def results_page(context):
    context.results_page = SearchResultsPage(context.driver)
    return context.results_page


def filters_page(context):
    context.filters_page = FiltersPage(context.driver)
    return context.filters_page


def property_page(context):
    context.property_page = PropertyDetailsPage(context.driver)
    return context.property_page


def is_end_to_end_scenario(context):
    scenario = getattr(context, "scenario", None)

    if not scenario:
        return False

    tags = set(
        getattr(
            scenario,
            "effective_tags",
            []
        )
    )

    return (
        "manual_otp" in tags
        or getattr(
            scenario.feature,
            "filename",
            ""
        ).endswith("end_to_end.feature")
    )


def capture(context, name, always=False):
    if (
            not always
            and not is_end_to_end_scenario(context)
    ):
        return

    with allure.step(f"Attach screenshot: {name}"):
        home_page(context).capture_screenshot(name)


def perform_search(context, location):
    with allure.step("Search Rental Property"):
        logger.info("Clicking Rent Tab")
        home_page(context).click_rent_tab()

        logger.info(f"Entering Location: {location}")
        home_page(context).enter_location(location)
        capture(context, "location_entered")

        logger.info("Clicking Search Button")
        home_page(context).click_search()

    context.results_page = SearchResultsPage(context.driver)

    with allure.step("Verify Search Results Page"):
        assert context.results_page.verify_search_results()
        capture(context, "search_results_page")

    context.filters_page = FiltersPage(context.driver)
    context.filters_page.click_ok_understood()

    return context.results_page


@when("I log in using the test data mobile number")
def step_login_using_test_data_mobile_number(context):
    with allure.step("Login Into 99acres"):
        login = login_page(context)

        logger.info("Hovering Profile Icon")
        login.hover_profile_icon()

        logger.info("Clicking Login/Register")
        login.click_login_register()
        capture(context, "login_popup")

        logger.info("Entering Mobile Number")
        login.enter_mobile_number(
            context.test_data["mobile_number"]
        )

        logger.info("Clicking Continue")
        login.click_continue()
        capture(context, "mobile_number_submitted")


@when("I wait {seconds:d} seconds for manual OTP entry")
def step_wait_for_manual_otp(context, seconds):
    logger.info(
        f"Waiting {seconds} seconds for manual OTP entry"
    )
    time.sleep(seconds)
    capture(context, "manual_otp_entered")


@when("I verify the OTP and continue")
def step_verify_otp_and_continue(context):
    login_page(context).click_verify_and_continue()
    login_page(context).wait_for_overlay_to_disappear()
    capture(context, "login_screenshot")


@then("the search results page should be displayed")
def step_verify_search_results_page(context):
    assert results_page(context).verify_search_results()
    capture(context, "search_results_verified")
