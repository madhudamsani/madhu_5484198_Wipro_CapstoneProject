from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException
)

from selenium.webdriver.common.by import By

from selenium.webdriver.support import (
    expected_conditions as EC
)

from selenium.webdriver.support.ui import (
    WebDriverWait
)

from utilities.config_reader import (
    get_implicit_wait
)


class PropertyDetailsPage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            40
        )

    # =========================
    # POPUPS
    # =========================

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

    # =========================
    # LOCATORS
    # =========================

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

    # =========================
    # COMMON METHODS
    # =========================

    def click_visible_if_present(
            self,
            locator,
            timeout=3
    ):

        self.driver.implicitly_wait(0)

        try:

            elements = WebDriverWait(
                self.driver,
                timeout
            ).until(
                EC.visibility_of_any_elements_located(
                    locator
                )
            )

            visible_elements = [
                element
                for element in elements
                if element.is_displayed()
            ]

            if not visible_elements:
                return False

            visible_elements.sort(
                key=lambda element: (
                    element.size.get("height", 0)
                    * element.size.get("width", 0)
                ),
                reverse=True
            )

            visible_element = visible_elements[0]

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center'
                });
                """,
                visible_element
            )

            try:

                visible_element.click()

            except WebDriverException:

                self.driver.execute_script(
                    "arguments[0].click();",
                    visible_element
                )

            try:

                WebDriverWait(
                    self.driver,
                    2
                ).until(
                    EC.invisibility_of_element(
                        visible_element
                    )
                )

            except TimeoutException:
                pass

            return True

        except (
            StaleElementReferenceException,
            TimeoutException
        ):

            return False

        finally:

            self.driver.implicitly_wait(
                get_implicit_wait()
            )

    def handle_blocking_popups(self):

        clicked = False

        for _ in range(3):

            clicked_this_round = (
                self.click_visible_if_present(
                    self.ok_understood_button
                )
                or self.click_visible_if_present(
                    self.cookie_ok_button
                )
            )

            clicked = (
                clicked
                or clicked_this_round
            )

            if not clicked_this_round:
                break

        return clicked

    def find_visible_element(
            self,
            locator,
            max_scrolls=8,
            timeout=10
    ):

        self.driver.implicitly_wait(0)

        try:

            for _ in range(max_scrolls):

                elements = self.driver.find_elements(
                    *locator
                )

                for element in elements:

                    try:

                        if element.is_displayed():

                            return element

                    except (
                        StaleElementReferenceException,
                        WebDriverException
                    ):
                        continue

                self.driver.execute_script(
                    "window.scrollBy(0, Math.floor(window.innerHeight * 0.55));"
                )

            return WebDriverWait(
                self.driver,
                timeout
            ).until(
                EC.visibility_of_element_located(
                    locator
                )
            )

        finally:

            self.driver.implicitly_wait(
                get_implicit_wait()
            )

    def scroll_to_and_click(
            self,
            element
    ):

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

    def click_detail_page_element(
            self,
            locator,
            max_scrolls=8
    ):

        self.handle_blocking_popups()

        element = self.find_visible_element(
            locator,
            max_scrolls=max_scrolls
        )

        self.scroll_to_and_click(
            element
        )

        self.handle_blocking_popups()

        return True

    # =========================
    # ACTIONS
    # =========================

    def switch_to_property_window(self):

        all_windows = (
            self.driver.window_handles
        )

        self.driver.switch_to.window(
            all_windows[-1]
        )

        self.wait.until(
            lambda driver:
            driver.current_url
            and driver.current_url != "about:blank"
        )

        self.handle_blocking_popups()

    def click_shortlist(self):

        return self.click_detail_page_element(
            self.shortlist_button,
            max_scrolls=3
        )

    def open_owner_details(self):

        return self.click_detail_page_element(
            self.owner_details_tab,
            max_scrolls=3
        )

    def click_view_phone_number(self):

        return self.click_detail_page_element(
            self.view_phone_button,
            max_scrolls=2
        )

    # =========================
    # VALIDATIONS
    # =========================

    def get_property_title(self):

        for locator in (
                self.property_title_locators
        ):

            try:

                elements = self.driver.find_elements(
                    *locator
                )

                for element in elements:

                    try:

                        if element.is_displayed():

                            text = (
                                element.text.strip()
                            )

                            if (
                                    text
                                    and len(text) > 5
                                    and len(text) < 200
                            ):

                                return text

                    except (
                        StaleElementReferenceException,
                        WebDriverException
                    ):
                        continue

            except (
                StaleElementReferenceException,
                WebDriverException
            ):
                continue

        return self.extract_title_from_body()

    def get_rent_amount(self):

        try:

            rent_element = self.wait.until(
                EC.visibility_of_element_located(
                    self.rent_amount
                )
            )

            rent_text = (
                rent_element.text.strip()
            )

            if rent_text:

                return rent_text

            raise TimeoutException(
                "Rent amount text is empty"
            )

        except TimeoutException:

            raise TimeoutException(
                "Rent amount was not found "
                "on the property details page"
            )

    def extract_title_from_body(self):

        body_text = self.driver.find_element(
            By.TAG_NAME,
            "body"
        ).text

        for line in body_text.splitlines():

            normalized_line = (
                line.strip()
            )

            if "for Rent" in normalized_line:

                return normalized_line

        return (
            body_text.splitlines()[0]
            .strip()
        )

    def verify_contact_section(self):

        element = self.find_visible_element(
            self.contact_section,
            max_scrolls=5,
            timeout=10
        )

        return element.is_displayed()