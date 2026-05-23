from selenium.webdriver.common.by import By


class LoginPageLocators:
    profile_icon = (
        By.XPATH,
        "//*[@id='app']/div/div[1]/div[2]/div[2]/div[5]"
    )

    login_register_button = (
        By.XPATH,
        "//div[contains(text(),'LOGIN / REGISTER')]"
    )

    mobile_input = (
        By.CSS_SELECTOR,
        "#app > div > div.component__dialogueBox > "
        "div.component__body > "
        "div.loginRegisterStyle__mobwebLoginGui > "
        "div > div > form > div.inputWrap__inputWrap > "
        "div > div > input"
    )

    continue_button = (
        By.XPATH,
        "//button[normalize-space()='Continue']"
    )

    verify_continue_button = (
        By.XPATH,
        "//button[contains(.,'Verify')]"
    )

    login_overlay = (
        By.CSS_SELECTOR,
        ".component__overlayBg"
    )
