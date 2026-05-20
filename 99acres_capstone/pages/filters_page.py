import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException
)

from selenium.webdriver.support.ui import (
    WebDriverWait
)

from selenium.webdriver.support import (
    expected_conditions as EC
)

from utilities.config_reader import (
    get_implicit_wait
)


class FiltersPage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            get_implicit_wait()
        )

    # =====================================================
    # POPUP LOCATORS
    # =====================================================

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

    # =====================================================
    # FILTER LOCATORS
    # =====================================================

    # 2 BHK
    bhk_2_filter = (
        By.XPATH,
        "//*[not(ancestor::*[@data-label='SEARCH']) "
        "and normalize-space()='2 BHK']"
    )

    # Flat / Apartment
    flat_apartment_filter = (
        By.XPATH,
        "//*[not(ancestor::*[@data-label='SEARCH']) "
        "and (normalize-space()='Residential Apartment' "
        "or normalize-space()='+ Residential Apartment' "
        "or normalize-space()='Flat/Apartment' "
        "or normalize-space()='+ Flat/Apartment')]"
    )

    # Owner
    owner_filter = (
        By.XPATH,
        "//*[not(ancestor::*[@data-label='SEARCH']) "
        "and normalize-space()='Owner']"
    )

    # Single Men
    single_men_filter = (
        By.XPATH,
        "//*[not(ancestor::*[@data-label='SEARCH']) "
        "and (normalize-space()='Single Men' "
        "or normalize-space()='+ Single Men')]"
    )

    # Sort Dropdown
    sort_by_dropdown = (
        By.ID,
        "sortby"
    )

    # Price Low To High
    price_low_to_high_option = (
        By.XPATH,
        "//*[self::div or self::span or self::li]"
        "[string-length(normalize-space()) <= 40 "
        "and (contains(normalize-space(),'Price (Low to High)') "
        "or contains(normalize-space(),'Price Low to High') "
        "or contains(normalize-space(),'Price: Low to High') "
        "or contains(normalize-space(),'Low to High'))]"
    )

    # =====================================================
    # APPLIED FILTERS
    # =====================================================

    applied_filters = (
        By.XPATH,
        "//*[contains(@class,'tag') "
        "or contains(@class,'applied')]"
    )

    applied_filters_heading = (
        By.XPATH,
        "//*[normalize-space()='Applied Filters']"
    )

    # =====================================================
    # PROPERTY RESULTS
    # =====================================================

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

    loading_placeholder = (
        By.CSS_SELECTOR,
        ".pageComponent.loadingPlaceholder, "
        "[class*='loadingPlaceholder']"
    )

    # =====================================================
    # COMMON METHODS
    # =====================================================

    def scroll_to_and_click(self, element):

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center'
            });
            """,
            element
        )

        try:

            ActionChains(
                self.driver
            ).move_to_element(
                element
            ).pause(
                0.1
            ).click().perform()

        except WebDriverException:

            self.driver.execute_script(
                "arguments[0].click();",
                element
            )

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

            visible_element = visible_elements[0]

            self.scroll_to_and_click(
                visible_element
            )

            return True

        except (
            TimeoutException,
            StaleElementReferenceException
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

    def click_ok_understood(self):

        return self.handle_blocking_popups()

    def get_visible_property_cards(self):

        cards = self.driver.find_elements(
            *self.property_cards
        )

        visible_cards = []

        for card in cards:

            try:

                if card.is_displayed():

                    visible_cards.append(
                        card
                    )

            except StaleElementReferenceException:
                continue

        return visible_cards

    def wait_for_filter_update_completion(
            self,
            previous_count,
            timeout=8
    ):
        """
        Wait until results refresh
        after applying filter.
        """

        try:

            WebDriverWait(
                self.driver,
                timeout
            ).until(
                lambda driver:
                self.get_results_count()
                != previous_count
            )

        except TimeoutException:
            pass

    def find_visible_filter_element(
            self,
            locator,
            timeout=10,
            max_scrolls=10
    ):

        self.driver.implicitly_wait(0)

        try:

            deadline = (
                time.time()
                + timeout
            )

            for _ in range(max_scrolls):

                elements = self.driver.find_elements(
                    *locator
                )

                visible_elements = []

                for element in elements:

                    try:

                        if (
                            element.is_displayed()
                            and element.size.get("height", 0) > 0
                            and element.size.get("width", 0) > 0
                        ):

                            visible_elements.append(
                                element
                            )

                    except StaleElementReferenceException:
                        continue

                if visible_elements:

                    visible_elements.sort(
                        key=lambda element:
                        element.location.get("y", 0)
                    )

                    return visible_elements[0]

                if time.time() >= deadline:
                    break

                self.driver.execute_script(
                    "window.scrollBy(0, Math.floor(window.innerHeight * 0.55));"
                )

                time.sleep(0.4)

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

    def click_filter_until_applied(
            self,
            locator,
            filter_name,
            retries=3,
            max_scrolls=10
    ):

        for _ in range(retries):

            previous_count = (
                self.get_results_count()
            )

            self.handle_blocking_popups()

            filter_element = (
                self.find_visible_filter_element(
                    locator,
                    max_scrolls=max_scrolls
                )
            )

            self.scroll_to_and_click(
                filter_element
            )

            self.wait_for_filter_update_completion(
                previous_count
            )

            if self.is_applied_filter_present(
                    filter_name
            ):
                return True

        raise AssertionError(
            f"Failed to apply filter: "
            f"{filter_name}"
        )

    # =====================================================
    # FILTER VALIDATIONS
    # =====================================================

    def is_applied_filter_present(
            self,
            filter_name
    ):

        body_text = self.driver.find_element(
            By.TAG_NAME,
            "body"
        ).text

        if "Applied Filters" in body_text:

            applied_section = body_text.split(
                "Applied Filters",
                1
            )[1]

            for section_end in (
                "Budget",
                "No. of Bedrooms",
                "Type of property"
            ):

                if section_end in applied_section:

                    applied_section = applied_section.split(
                        section_end,
                        1
                    )[0]

                    break

            return filter_name in applied_section

        return False

    def verify_required_filters_applied(self):

        required_filters = [
            "2 BHK",
            "Flat/Apartment",
            "Owner",
            "Single Men"
        ]

        return all(
            self.is_applied_filter_present(
                filter_name
            )
            for filter_name in required_filters
        )

    # =====================================================
    # FILTER METHODS
    # =====================================================

    def apply_2_bhk_filter(self):

        return self.click_filter_until_applied(
            self.bhk_2_filter,
            "2 BHK",
            max_scrolls=4
        )

    def apply_flat_apartment_filter(self):

        return self.click_filter_until_applied(
            self.flat_apartment_filter,
            "Flat/Apartment",
            max_scrolls=8
        )

    def apply_owner_filter(self):

        return self.click_filter_until_applied(
            self.owner_filter,
            "Owner",
            max_scrolls=4
        )

    def apply_single_men_filter(self):

        return self.click_filter_until_applied(
            self.single_men_filter,
            "Single Men",
            max_scrolls=10
        )

    def sort_price_low_to_high(self):

        self.scroll_to_page_top()

        self.handle_blocking_popups()

        dropdown = (
            self.find_visible_filter_element(
                self.sort_by_dropdown
            )
        )

        self.scroll_to_and_click(
            dropdown
        )

        option = (
            self.find_visible_filter_element(
                self.price_low_to_high_option
            )
        )

        self.scroll_to_and_click(
            option
        )

        return True

    def scroll_to_page_top(self):

        self.driver.execute_script(
            """
            window.scrollTo(0, 0);
            document.documentElement.scrollTop = 0;
            document.body.scrollTop = 0;
            """
        )

        ActionChains(
            self.driver
        ).send_keys(
            Keys.HOME
        ).perform()

        time.sleep(0.5)

    # =====================================================
    # RESULTS VALIDATIONS
    # =====================================================

    def verify_filtered_results(self):

        results = self.wait.until(
            EC.visibility_of_any_elements_located(
                self.property_cards
            )
        )

        return len(results) > 0

    def get_results_count(self):

        results = (
            self.get_visible_property_cards()
        )

        return len(results)

    # =====================================================
    # PROPERTY SELECTION
    # =====================================================

    def get_first_result_card(self):

        return self.wait.until(
            lambda driver:
            self.get_visible_property_cards()[0]
            if self.get_visible_property_cards()
            else False
        )

    def get_first_result_click_target(self):

        first_result = (
            self.get_first_result_card()
        )

        links = first_result.find_elements(
            *self.property_link_inside_card
        )

        for link in links:

            try:

                href = link.get_attribute(
                    "href"
                )

                if (
                    href
                    and href.startswith("http")
                    and link.is_displayed()
                ):

                    return link

            except StaleElementReferenceException:
                continue

        return first_result

    def select_first_result(self):

        self.handle_blocking_popups()

        first_result_target = (
            self.get_first_result_click_target()
        )

        self.scroll_to_and_click(
            first_result_target
        )

        return True

    def verify_property_detail_page_opened(self):

        self.wait.until(
            lambda driver:
            driver.current_url
            and driver.current_url != "about:blank"
        )

        page_text = self.driver.find_element(
            By.TAG_NAME,
            "body"
        ).text

        return (
            "99acres" in self.driver.current_url
            and (
                "Property" in page_text
                or "Bedroom" in page_text
                or "Contact" in page_text
                or "View Number" in page_text
            )
        )
