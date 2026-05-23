from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import re
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

from config.config import (
    get_implicit_wait
)
from locators.filters_page_locators import FiltersPageLocators


class FiltersPage(FiltersPageLocators):

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            get_implicit_wait()
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

        for _ in range(2):

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
            max_scrolls=4
    ):

        self.driver.implicitly_wait(0)

        try:

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

                self.driver.execute_script(
                    "window.scrollBy(0, Math.floor(window.innerHeight * 0.55));"
                )

                try:

                    WebDriverWait(
                        self.driver,
                        2
                    ).until(
                        lambda driver:
                        len(
                            self.driver.find_elements(
                                *locator
                            )
                        ) > 0
                    )

                except TimeoutException:
                    pass

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
            filter_names,
            retries=3,
            max_scrolls=5
    ):

        if isinstance(filter_names, str):
            filter_names = [filter_names]

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

            if any(
                    self.is_applied_filter_present(name)
                    for name in filter_names
            ):
                return True

        raise AssertionError(
            f"Failed to apply filter: "
            f"{' / '.join(filter_names)}"
        )

    # =====================================================
    # FILTER VALIDATIONS
    # =====================================================

    def is_applied_filter_present(
            self,
            filter_name
    ):

        body_text = self.driver.find_element(
            *self.body
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

        flat_apartment_present = any(
            self.is_applied_filter_present(filter_name)
            for filter_name in [
                "Flat/Apartment",
                "Residential Apartment",
                "Apartment"
            ]
        )

        return (
                self.is_applied_filter_present("2 BHK")
                and flat_apartment_present
                and self.is_applied_filter_present("Owner")
                and self.is_applied_filter_present("Single Men")
        )

    # =====================================================
    # FILTER METHODS
    # =====================================================

    def apply_2_bhk_filter(self):

        return self.click_filter_until_applied(
            self.bhk_2_filter,
            "2 BHK",
            max_scrolls=2
        )

    def apply_flat_apartment_filter(self):

        return self.click_filter_until_applied(
            self.flat_apartment_filter,
            [
                "Flat/Apartment",
                "Residential Apartment",
                "Apartment"
            ],
            max_scrolls=4
        )

    def apply_owner_filter(self):

        return self.click_filter_until_applied(
            self.owner_filter,
            "Owner",
            max_scrolls=2
        )

    def apply_single_men_filter(self):

        return self.click_filter_until_applied(
            self.single_men_filter,
            "Single Men",
            max_scrolls=5
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

        try:

            WebDriverWait(
                self.driver,
                3
            ).until(
                lambda driver:
                driver.execute_script(
                    "return window.pageYOffset"
                ) == 0
            )

        except TimeoutException:
            pass

    # =====================================================
    # RESULTS VALIDATIONS
    # =====================================================

    def verify_filtered_results(self):

        self.wait.until(
            EC.visibility_of_any_elements_located(
                self.property_cards
            )
        )

        return True

    def get_results_count(self):

        try:

            count_element = self.wait.until(
                EC.visibility_of_element_located(
                    self.filtered_results_count
                )
            )

            count_text = (
                count_element.text.strip()
            )

            count_number = (
                ''.join(
                    filter(
                        str.isdigit,
                        count_text
                    )
                )
            )

            return int(count_number)

        except (
                TimeoutException,
                ValueError
        ):

            return 0

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
            *self.body
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

#     return bhk_text
    def get_bhk_text(self):

        full_title = self.driver.find_element(
            *self.bhk2_title
        ).text.strip()

        match = re.search(r"\d+\s*BHK", full_title)

        return match.group(0) if match else None
