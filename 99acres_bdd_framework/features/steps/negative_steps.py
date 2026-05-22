from behave import given, then, when

from features.steps.common_steps import (
    capture,
    home_page,
    logger,
    property_page
)


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
