from selenium.webdriver.common.by import By


class SearchResultsPageLocators:
    results_heading = (
        By.TAG_NAME,
        "h1"
    )

    property_cards = (
        By.CSS_SELECTOR,
        "div[data-label='SEARCH']"
    )

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
