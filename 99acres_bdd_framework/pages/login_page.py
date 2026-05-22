from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException
)

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.config import (
    get_implicit_wait
)


class LoginPage:
    """
    Page Object Model for 99acres Login Page.

    Handles:
    - Login/Register popup
    - Mobile number entry
    - OTP verification flow
    - Overlay synchronization
    """

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            get_implicit_wait()
        )

        self.actions = ActionChains(driver)

    # =====================================================
    # LOCATORS
    # =====================================================

    # Profile Icon
    profile_icon = (
        By.XPATH,
        "//*[@id='app']/div/div[1]/div[2]/div[2]/div[5]"
    )

    # Login/Register Button
    login_register_button = (
        By.XPATH,
        "//div[contains(text(),'LOGIN / REGISTER')]"
    )

    # Mobile Number Input
    mobile_input = (
        By.CSS_SELECTOR,
        "#app > div > div.component__dialogueBox > "
        "div.component__body > "
        "div.loginRegisterStyle__mobwebLoginGui > "
        "div > div > form > div.inputWrap__inputWrap > "
        "div > div > input"
    )

    # Continue Button
    continue_button = (
        By.XPATH,
        "//button[normalize-space()='Continue']"
    )

    # Verify & Continue Button
    verify_continue_button = (
        By.XPATH,
        "//button[contains(.,'Verify')]"
    )

    # Overlay Popup
    login_overlay = (
        By.CSS_SELECTOR,
        ".component__overlayBg"
    )

    # =====================================================
    # COMMON METHODS
    # =====================================================

    def safe_click(self, locator):
        """
        Generic reusable safe click method.

        Features:
        - Waits until clickable
        - Scrolls element into view
        - Handles JS click fallback
        """

        try:

            element = self.wait.until(
                EC.element_to_be_clickable(
                    locator
                )
            )

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center'
                });
                """,
                element
            )

            try:

                element.click()

            except WebDriverException:

                self.driver.execute_script(
                    "arguments[0].click();",
                    element
                )

        except TimeoutException as error:

            raise AssertionError(
                f"Element not clickable: {locator}"
            ) from error

    # =====================================================
    # ACTIONS
    # =====================================================

    def hover_profile_icon(self):
        """
        Hover over profile icon
        to reveal login/register option.
        """

        try:

            profile = self.wait.until(
                EC.visibility_of_element_located(
                    self.profile_icon
                )
            )

            self.actions.move_to_element(
                profile
            ).perform()

        except TimeoutException as error:

            raise AssertionError(
                "Profile icon not visible"
            ) from error

    def click_login_register(self):
        """
        Click Login/Register button.
        """

        self.safe_click(
            self.login_register_button
        )

    def enter_mobile_number(self, mobile):
        """
        Enter mobile number
        into login popup.
        """

        try:

            mobile_field = self.wait.until(
                EC.visibility_of_element_located(
                    self.mobile_input
                )
            )

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center'
                });
                """,
                mobile_field
            )

            mobile_field.click()

            mobile_field.clear()

            mobile_field.send_keys(
                str(mobile)
            )

        except TimeoutException as error:

            raise AssertionError(
                "Mobile number input field not found"
            ) from error

    def click_continue(self):
        """
        Click Continue button
        after entering mobile number.
        """

        self.safe_click(
            self.continue_button
        )

    def click_verify_and_continue(self):
        """
        Click Verify & Continue button
        after manual OTP entry.
        """

        self.safe_click(
            self.verify_continue_button
        )

    # =====================================================
    # OVERLAY HANDLING
    # =====================================================

    def wait_for_overlay_to_disappear(self):
        """
        Wait for login overlay/popup
        to disappear after login.
        """

        try:

            self.wait.until(
                EC.invisibility_of_element_located(
                    self.login_overlay
                )
            )

        except TimeoutException:

            # Overlay may already disappear
            # Ignore timeout safely
            pass
