import os
from datetime import datetime
import allure
import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from utilities.config_reader import (
    get_base_url,
    get_browser,
    get_implicit_wait
)
from utilities.logger import LogGen

logger = LogGen.loggen()

@pytest.fixture(scope="function")
def driver():

    browser = get_browser()

    if browser == "chrome":

        chrome_options = Options()

        chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )

        chrome_options.add_experimental_option(
            "excludeSwitches",
            ["enable-automation"]
        )

        chrome_options.add_experimental_option(
            "useAutomationExtension",
            False
        )

        logger.info(
            "Launching Chrome Browser"
        )
        driver = webdriver.Chrome(
            service=Service(),options=chrome_options
        )

        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )


    elif browser == "edge":

        driver = webdriver.Edge()

    else:
        raise Exception("Browser not supported")

    driver.maximize_window()

    driver.implicitly_wait(get_implicit_wait())

    driver.get(get_base_url())

    logger.info(
        "Navigated To 99acres Website"
    )
    yield driver

    logger.info(
        "Closing Browser"
    )
    driver.quit()
    logger.info(
        "Browser Closed Successfully"
    )

    


# Screenshot on failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = item.funcargs.get("driver", None)

        if driver:

            screenshots_dir = "screenshots"

            os.makedirs(screenshots_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            file_name = f"{item.name}_{timestamp}.png"

            file_path = os.path.join(
                screenshots_dir,
                file_name
            )

            try:
                driver.save_screenshot(file_path)

                print(f"Screenshot saved: {file_path}")

            except WebDriverException as error:
                print(f"Screenshot could not be saved: {error}")
