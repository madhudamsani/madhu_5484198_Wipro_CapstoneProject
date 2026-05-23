import os

from datetime import datetime
from pathlib import Path

import allure

from selenium import webdriver

from selenium.common.exceptions import (
    WebDriverException
)

from selenium.webdriver.chrome.options import (
    Options
)

from config.config import (
    get_base_url,
    get_browser,
    get_implicit_wait
)

from utilities.excel_reader import (
    get_test_data
)

from utilities.logger import (
    LogGen
)


logger = LogGen.loggen()

# =====================================================
# PROJECT PATHS
# =====================================================

PROJECT_ROOT = (
    Path(__file__).resolve().parents[1]
)

REPORTS_DIR = (
    PROJECT_ROOT / "reports"
)

ALLURE_RESULTS_DIR = (
    REPORTS_DIR / "allure-results"
)

ALLURE_REPORT_DIR = (
    REPORTS_DIR / "allure-report"
)

SCREENSHOTS_DIR = (
    PROJECT_ROOT / "screenshots"
)

LOGS_DIR = (
    PROJECT_ROOT / "logs"
)

LOG_FILE = (
    LOGS_DIR / "automation.log"
)

# =====================================================
# BEFORE ALL
# =====================================================

def before_all(context):

    required_directories = [

        ALLURE_RESULTS_DIR,
        ALLURE_REPORT_DIR,
        SCREENSHOTS_DIR,
        LOGS_DIR
    ]

    for folder in required_directories:

        os.makedirs(
            folder,
            exist_ok=True
        )

    environment_file = (
        ALLURE_RESULTS_DIR
        / "environment.properties"
    )

    environment_file.write_text(

        "\n".join(

            [

                f"Base_URL={get_base_url()}",
                f"Browser={get_browser()}",
                f"Implicit_Wait={get_implicit_wait()}",
                "Framework=Behave BDD",
                "Application=99acres"
            ]

        ),

        encoding="utf-8"
    )

    logger.info(
        "Framework Initialization Completed"
    )

# =====================================================
# BEFORE SCENARIO
# =====================================================

def before_scenario(
        context,
        scenario
):

    context.scenario_log_start_position = (
        get_log_file_size()
    )

    logger.info(
        f"Starting Scenario: "
        f"{scenario.name}"
    )

    browser = (
        get_browser().lower()
    )

    if browser == "chrome":

        chrome_options = Options()

        chrome_options.add_argument(
            "--start-maximized"
        )

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

        context.driver = webdriver.Chrome(
            options=chrome_options
        )

        context.driver.execute_script(
            """
            Object.defineProperty(
                navigator,
                'webdriver',
                {
                    get: () => undefined
                }
            )
            """
        )

    elif browser == "edge":

        context.driver = webdriver.Edge()

        context.driver.maximize_window()

    else:

        raise ValueError(
            f"Unsupported Browser: "
            f"{browser}"
        )

    context.driver.implicitly_wait(
        get_implicit_wait()
    )

    context.driver.get(
        get_base_url()
    )

    context.test_data = (
        get_test_data()
    )

    logger.info(
        "Navigated To 99acres Website"
    )

# =====================================================
# AFTER STEP
# =====================================================

def after_step(
        context,
        step
):

    step_status = (
        str(step.status).lower()
    )

    if (
            "failed" not in step_status
            and "error" not in step_status
    ):

        return

    if not hasattr(
            context,
            "driver"
    ):

        return

    attach_failure_screenshot(
        context,
        step.name,
        "Failed Step Screenshot"
    )

# =====================================================
# AFTER SCENARIO
# =====================================================

def after_scenario(
        context,
        scenario
):

    logger.info(
        f"Ending Scenario: "
        f"{scenario.name}"
    )

    scenario_status = (
        str(scenario.status).lower()
    )

    if (
            "failed" in scenario_status
            or "error" in scenario_status
    ):

        attach_failure_screenshot(
            context,
            scenario.name,
            "Failed Scenario Screenshot"
        )

    try:

        if hasattr(
                context,
                "driver"
        ):

            context.driver.quit()

            logger.info(
                "Browser Closed Successfully"
            )

    except Exception as error:

        logger.error(
            f"Error While Closing Browser: "
            f"{error}"
        )

    attach_scenario_logs(
        context,
        scenario.name
    )

# =====================================================
# COMMON FAILURE SCREENSHOT METHOD
# =====================================================

def attach_failure_screenshot(
        context,
        name,
        log_message
):

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    screenshot_name = (

        f"{name}_{timestamp}"

        .replace(" ", "_")
        .replace("/", "_")
    )

    screenshot_file = os.path.join(

        SCREENSHOTS_DIR,

        f"{screenshot_name}.png"
    )

    try:

        context.driver.save_screenshot(
            screenshot_file
        )

        allure.attach.file(

            screenshot_file,

            name=screenshot_name,

            attachment_type=
            allure.attachment_type.PNG
        )

        logger.info(
            f"{log_message}: "
            f"{screenshot_file}"
        )

    except WebDriverException as error:

        logger.error(
            f"Unable To Save Screenshot: "
            f"{error}"
        )


# =====================================================
# COMMON ALLURE LOG ATTACHMENT METHODS
# =====================================================

def get_log_file_size():

    if not LOG_FILE.exists():

        return 0

    return LOG_FILE.stat().st_size


def flush_logger_handlers():

    for handler in logger.handlers:

        handler.flush()


def attach_scenario_logs(
        context,
        scenario_name
):

    flush_logger_handlers()

    if not LOG_FILE.exists():

        return

    start_position = getattr(
        context,
        "scenario_log_start_position",
        0
    )

    try:

        with LOG_FILE.open(
                "r",
                encoding="utf-8",
                errors="replace"
        ) as log_file:

            log_file.seek(
                start_position
            )

            scenario_logs = (
                log_file.read()
                .strip()
            )

        if not scenario_logs:

            return

        attachment_name = (
            f"{scenario_name}_logs"
            .replace(" ", "_")
            .replace("/", "_")
        )

        allure.attach(
            scenario_logs,
            name=attachment_name,
            attachment_type=allure.attachment_type.TEXT
        )

    except OSError as error:

        logger.error(
            f"Unable To Attach Scenario Logs: "
            f"{error}"
        )
