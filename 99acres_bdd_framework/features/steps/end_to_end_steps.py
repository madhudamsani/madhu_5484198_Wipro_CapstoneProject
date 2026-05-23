import time

import allure
from behave import given, then, when

from pages.filters_page import FiltersPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.property_details_page import PropertyDetailsPage
from pages.search_results_page import SearchResultsPage
from utilities.logger import LogGen


logger = LogGen.loggen()

END_TO_END_SCREENSHOTS = {
    "login_popup",
    "manual_otp_entered",
    "location_entered",
    "search_results_page",
    "all_filters_applied",
    "property_details_page",
    "shortlist_clicked",
    "owner_details"
}


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
        "end_to_end" in tags
        or getattr(
            scenario.feature,
            "filename",
            ""
        ).endswith("end_to_end.feature")
    )


def capture(context, name, always=False):
    is_end_to_end = is_end_to_end_scenario(context)

    if is_end_to_end and name not in END_TO_END_SCREENSHOTS:
        return

    if not always and not is_end_to_end:
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
        login.enter_mobile_number(context.test_data["mobile_number"])

        logger.info("Clicking Continue")
        login.click_continue()


@when("I wait {seconds:d} seconds for manual OTP entry")
def step_wait_for_manual_otp(context, seconds):
    logger.info(f"Waiting {seconds} seconds for manual OTP entry")
    time.sleep(seconds)
    capture(context, "manual_otp_entered")


@when("I verify the OTP and continue")
def step_verify_otp_and_continue(context):
    login_page(context).click_verify_and_continue()
    login_page(context).wait_for_overlay_to_disappear()


@given("I have searched rental properties using the test data location")
@when("I search rental properties using the test data location")
def step_search_using_test_data_location(context):
    context.location = context.test_data["location"]
    perform_search(context, context.location)


@then("the search results page should be displayed")
def step_verify_search_results_page(context):
    assert results_page(context).verify_search_results()


@when("I close blocking popups on the search results page")
def step_close_search_result_popups(context):
    filters_page(context).click_ok_understood()


@when("I apply the 2 BHK filter")
def step_apply_2_bhk_filter(context):
    assert filters_page(context).apply_2_bhk_filter()


@when("I apply the Flat/Apartment filter")
def step_apply_flat_apartment_filter(context):
    assert filters_page(context).apply_flat_apartment_filter()


@when("I apply the Owner filter")
def step_apply_owner_filter(context):
    assert filters_page(context).apply_owner_filter()


@when("I apply the Single Men filter")
def step_apply_single_men_filter(context):
    assert filters_page(context).apply_single_men_filter()


@when("I sort results by price low to high")
def step_sort_price_low_to_high(context):
    assert filters_page(context).sort_price_low_to_high()


@then("all required filters should be applied")
def step_verify_all_required_filters_are_applied(context):
    assert filters_page(context).verify_required_filters_applied()
    capture(context, "all_filters_applied", always=True)


@then("filtered results should be visible")
def step_verify_filtered_results_visible(context):
    assert filters_page(context).verify_filtered_results()


@when("I open the first property from search results")
def step_open_first_property(context):
    assert filters_page(context).select_first_result()


@when("I switch to the property details window")
def step_switch_to_property_details_window(context):
    property_page(context).switch_to_property_window()
    capture(context, "property_details_page")


@then("the property title and rent amount should be visible")
def step_verify_property_title_and_rent(context):
    property_details = property_page(context)

    title = property_details.get_property_title()
    rent = property_details.get_rent_amount()

    logger.info(f"Property Title: {title[:150]}")
    logger.info(f"Rent Amount: {rent}")

    assert title is not None and len(title) > 0
    assert rent is not None and len(rent) > 0
    capture(context, "property_details_verified", always=True)


@when("I click the shortlist button")
def step_click_shortlist_button(context):
    property_page(context).handle_blocking_popups()
    assert property_page(context).click_shortlist()
    capture(context, "shortlist_clicked")


@when("I open the owner details section")
def step_open_owner_details_section(context):
    property_page(context).handle_blocking_popups()
    assert property_page(context).open_owner_details()


@when("I click the view phone number button")
def step_click_view_phone_number_button(context):
    assert property_page(context).click_view_phone_number()


@then("the contact section should be displayed")
def step_verify_contact_section_displayed(context):
    assert property_page(context).verify_contact_section()
    property_page(context).close_fraud_alert_popup()
    capture(context, "owner_details", always=True)
