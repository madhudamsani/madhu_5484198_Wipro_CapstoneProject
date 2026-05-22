from behave import given, then, when

from features.steps.common_steps import (
    capture,
    filters_page,
    home_page,
    logger,
    perform_search,
    property_page,
    results_page
)


@given("I have searched rental properties using the test data location")
@when("I search rental properties using the test data location")
def step_search_using_test_data_location(context):
    context.location = context.test_data["location"]
    perform_search(context, context.location)


@when("I open the first property from search results")
def step_open_first_property(context):
    assert filters_page(context).select_first_result()
    capture(context, "first_property_opened")


@when("I switch to the property details window")
def step_switch_to_property_details_window(context):
    property_page(context).switch_to_property_window()
    capture(context, "property_details_page")


@when("I click the shortlist button")
def step_click_shortlist_button(context):
    property_page(context).handle_blocking_popups()
    assert property_page(context).click_shortlist()
    capture(context, "shortlist_clicked")


@when("I open the owner details section")
def step_open_owner_details_section(context):
    property_page(context).handle_blocking_popups()
    assert property_page(context).open_owner_details()
    capture(context, "owner_details_opened")


@when("I click the view phone number button")
def step_click_view_phone_number_button(context):
    assert property_page(context).click_view_phone_number()
    capture(context, "view_phone_number_clicked")


@then('the results heading should contain "{expected_text}"')
def step_verify_results_heading_contains(context, expected_text):
    heading = results_page(context).get_results_heading()
    logger.info(f"Results Heading: {heading}")
    assert expected_text.lower() in heading.lower()
    capture(context, "results_heading_verified", always=True)


@then("the search bar should display the searched location")
def step_verify_search_bar_location(context):
    displayed_location = home_page(context).get_displayed_location()
    expected_location = (
        context.test_data["location"]
        .lower()
        .replace("rent in", "")
        .strip()
    )

    logger.info(f"Displayed Location: {displayed_location}")
    assert displayed_location.lower() == expected_location
    capture(context, "search_location_displayed", always=True)


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


@then("the contact section should be displayed")
def step_verify_contact_section_displayed(context):
    assert property_page(context).verify_contact_section()
    property_page(context).close_fraud_alert_popup()
    capture(context, "owner_details", always=True)
