from behave import given, then, when

from features.steps.end_to_end_steps import (
    capture,
    filters_page,
    home_page,
    logger,
    property_page,
    results_page
)


@then('the results heading should contain "{expected_text}"') #Rent
def step_verify_results_heading_contains(context, expected_text):
    heading = results_page(context).get_results_heading()
    logger.info(f"Results Heading: {heading}")
    assert expected_text.lower() in heading.lower()
    capture(context, "results_heading_verified", always=True)


@then('the "{filter_name}" filter should be applied')
def step_verify_named_filter_is_applied(context, filter_name):
    assert filters_page(context).is_applied_filter_present(
        filter_name
    )
    capture(
        context,
        f"{filter_name.lower().replace('/', '_').replace(' ', '_')}_filter_verified",
        always=True
    )


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


@given("I remember the current page URL")
def step_remember_current_url(context):
    context.initial_url = context.driver.current_url


@when("I select the Rent tab")
def step_select_rent_tab(context):
    home_page(context).click_rent_tab()


@when("I submit the search without a location")
def step_submit_search_without_location(context):
    home_page(context).click_search()


@then("the login popup should be displayed")
def step_verify_login_popup_displayed(context):
    assert property_page(context).is_login_popup_displayed()
    capture(context, "shortlist_login_popup", always=True)


@then("I should remain on the same page")
def step_verify_same_page(context):
    current_url = context.driver.current_url
    logger.info(f"Initial URL: {context.initial_url}")
    logger.info(f"Current URL: {current_url}")
    assert current_url == context.initial_url
    capture(context, "empty_location_validation", always=True)
