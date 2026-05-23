from selenium.webdriver.common.by import By


class FiltersPageLocators:
    body = (
        By.TAG_NAME,
        "body"
    )

    ok_understood_button = (
        By.XPATH,
        "//*[self::button or self::div or self::span]"
        "[translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')="
        "'ok, understood']"
    )

    cookie_ok_button = (
        By.XPATH,
        "//*["
        "(self::button or self::div or self::span)"
        " and (normalize-space()='Okay' "
        "or normalize-space()='OK')"
        "]"
    )

    bhk_2_filter = (
        By.XPATH,
        "//*[not(ancestor::*[@data-label='SEARCH']) "
        "and normalize-space()='2 BHK']"
    )

    bhk2_title = (
        By.XPATH,
        "//*[@id='AI_LISTING']/div[2]/div[1]/div/div[2]/a/h2/span"
    )

    flat_apartment_filter = (
        By.XPATH,
        "//*[not(ancestor::*[@data-label='SEARCH']) "
        "and (normalize-space()='Residential Apartment' "
        "or normalize-space()='+ Residential Apartment' "
        "or normalize-space()='Flat/Apartment' "
        "or normalize-space()='+ Flat/Apartment')]"
    )

    owner_filter = (
        By.XPATH,
        "//*[not(ancestor::*[@data-label='SEARCH']) "
        "and normalize-space()='Owner']"
    )

    single_men_filter = (
        By.XPATH,
        "//*[not(ancestor::*[@data-label='SEARCH']) "
        "and (normalize-space()='Single Men' "
        "or normalize-space()='+ Single Men')]"
    )

    sort_by_dropdown = (
        By.ID,
        "sortby"
    )

    price_low_to_high_option = (
        By.XPATH,
        "//*[self::div or self::span or self::li]"
        "[string-length(normalize-space()) <= 40 "
        "and (contains(normalize-space(),'Price (Low to High)') "
        "or contains(normalize-space(),'Price Low to High') "
        "or contains(normalize-space(),'Price: Low to High') "
        "or contains(normalize-space(),'Low to High'))]"
    )

    property_cards = (
        By.CSS_SELECTOR,
        "div[data-label='SEARCH'], "
        "section[data-cnstrc-item-name='propertyTuple'], "
        "div[data-cnstrc-item-name='propertyTuple']"
    )

    property_link_inside_card = (
        By.CSS_SELECTOR,
        "a[href]"
    )

    filtered_results_count = (
        By.XPATH,
        "//*[@id='app']/div/div/div[4]/div[3]/div[1]/div[1]/span"
    )
