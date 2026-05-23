from selenium.webdriver.common.by import By


class PropertyDetailsPageLocators:
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
        "] | //button["
        "contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'accept') "
        "or contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'agree')]"
    )

    fraud_alert_close_button = (
        By.XPATH,
        "//*[@id='app']/div/div[5]/div/div[1]/i"
    )

    rent_amount = (
        By.ID,
        "pdPrice"
    )

    shortlist_button = (
        By.ID,
        "shortListBtn"
    )

    owner_details_tab = (
        By.XPATH,
        "//*[self::button or self::div or self::span or self::a]"
        "[contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'owner details')]"
    )

    view_phone_button = (
        By.XPATH,
        "//*[@id='OwnerDetails']/div/input"
    )

    contact_section = (
        By.XPATH,
        "//*[contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'contact') "
        "or contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'phone') "
        "or contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'login') "
        "or contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'register')]"
    )

    property_title_locators = [
        (
            By.XPATH,
            "//h1"
        ),
        (
            By.XPATH,
            "//h2"
        ),
        (
            By.XPATH,
            "//*[contains(text(),'for Rent')]"
        )
    ]
