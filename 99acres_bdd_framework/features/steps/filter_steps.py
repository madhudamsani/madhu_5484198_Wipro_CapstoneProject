from behave import then, when

from features.steps.common_steps import (
    capture,
    filters_page
)


@when("I close blocking popups on the search results page")
def step_close_search_result_popups(context):
    filters_page(context).click_ok_understood()
    capture(context, "blocking_popups_closed")


@when("I apply the 2 BHK filter")
def step_apply_2_bhk_filter(context):
    assert filters_page(context).apply_2_bhk_filter()
    capture(context, "2bhk_filter_applied")


@when("I apply the Flat/Apartment filter")
def step_apply_flat_apartment_filter(context):
    assert filters_page(context).apply_flat_apartment_filter()
    capture(context, "flat_apartment_filter_applied")


@when("I apply the Owner filter")
def step_apply_owner_filter(context):
    assert filters_page(context).apply_owner_filter()
    capture(context, "owner_filter_applied")


@when("I apply the Single Men filter")
def step_apply_single_men_filter(context):
    assert filters_page(context).apply_single_men_filter()
    capture(context, "single_men_filter_applied")


@when("I sort results by price low to high")
def step_sort_price_low_to_high(context):
    assert filters_page(context).sort_price_low_to_high()
    capture(context, "price_low_to_high_sort_applied")


@then("filtered results should be visible")
def step_verify_filtered_results_visible(context):
    assert filters_page(context).verify_filtered_results()
    capture(context, "filtered_results")


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


@then("all required filters should be applied")
def step_verify_all_required_filters_are_applied(context):
    assert filters_page(context).verify_required_filters_applied()
    capture(context, "all_filters_applied", always=True)
