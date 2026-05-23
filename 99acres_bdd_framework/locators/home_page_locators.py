from selenium.webdriver.common.by import By


class HomePageLocators:
    buy_tab = (
        By.ID,
        "inPageSearchForm_0"
    )

    rent_tab = (
        By.ID,
        "inPageSearchForm_1"
    )

    rent_tab_by_text = (
        By.XPATH,
        "//*[not(ancestor::*[@data-label='SEARCH']) "
        "and normalize-space()='Rent']"
    )

    search_box = (
        By.ID,
        "keyword2"
    )

    search_button = (
        By.ID,
        "searchform_search_btn"
    )

    search_button_by_text = (
        By.XPATH,
        "//button[normalize-space()='Search']"
    )

    displayed_location = (
        By.XPATH,
        "//*[@id='searchTabContainer']/div[1]/span[2]"
    )
