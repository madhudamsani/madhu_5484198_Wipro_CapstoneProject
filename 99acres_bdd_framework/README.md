# 99acres BDD Automation Framework

This project is a Python-based BDD UI automation framework for the 99acres real estate website. It uses Behave, Selenium WebDriver, the Page Object Model, separated locator classes, Excel-driven test data, logging, screenshots, and Allure reporting to validate rental-property search flows.

The framework focuses on the rent journey: opening 99acres, searching for rental properties by location, validating search results, applying filters, opening a property detail page, checking login-protected shortlist behavior, and completing an end-to-end owner-contact flow.

## Tech Stack

- Python 3.x
- Selenium WebDriver
- Behave BDD
- Gherkin feature files
- Allure Behave integration
- OpenPyXL for Excel test data
- Chrome by default, with Edge support in the Behave environment hook

## Project Structure

```text
99acres_bdd_framework/
|-- config/
|   |-- config.py
|   `-- __init__.py
|-- features/
|   |-- environment.py
|   |-- end_to_end.feature
|   |-- positive_flows.feature
|   |-- negative_flows.feature
|   `-- steps/
|       |-- end_to_end_steps.py
|       |-- positive_negative_steps.py
|       `-- __init__.py
|-- locators/
|   |-- home_page_locators.py
|   |-- login_page_locators.py
|   |-- search_results_page_locators.py
|   |-- filters_page_locators.py
|   |-- property_details_page_locators.py
|   `-- __init__.py
|-- pages/
|   |-- home_page.py
|   |-- login_page.py
|   |-- search_results_page.py
|   |-- filters_page.py
|   |-- property_details_page.py
|   `-- __init__.py
|-- test_data/
|   `-- test_data.xlsx
|-- utilities/
|   |-- excel_reader.py
|   |-- logger.py
|   `-- __init__.py
|-- reports/
|   |-- allure-results/
|   `-- allure-report/
|-- screenshots/
|-- logs/
|   `-- automation.log
|-- behave.ini
|-- requirements.txt
`-- README.md
```

## Core Flow

1. `behave.ini` points Behave to the `features/` folder and configures Allure result output.
2. `features/environment.py` creates required runtime folders before execution.
3. Before each scenario, the environment hook launches the configured browser and opens the 99acres base URL.
4. Test data is loaded from `test_data/test_data.xlsx` through `utilities/excel_reader.py`.
5. Gherkin scenarios call step definitions in `features/steps/`.
6. Step definitions call Page Object Model classes from `pages/`.
7. Page objects use locator classes from `locators/`.
8. Logs are written to `logs/automation.log`.
9. Failed steps and failed scenarios save screenshots in `screenshots/` and attach them to Allure.
10. Scenario-specific logs are attached to the Allure result files under `reports/allure-results/`.

## Important Files

### `behave.ini`

Configures Behave execution:

```ini
[behave]
paths = features
show_skipped = false
show_timings = true
format = allure_behave.formatter:AllureFormatter
outfiles = reports/allure-results
```

Because Allure formatting is configured here, a normal Behave run writes result files to `reports/allure-results`.

### `config/config.py`

Default runtime configuration:

```python
base_url = "https://www.99acres.com"
browser = "chrome"
implicit_wait = 15
```

Supported browser values in `features/environment.py` are `chrome` and `edge`.

### `features/environment.py`

Defines Behave lifecycle hooks. It:

- Creates `reports/allure-results`, `reports/allure-report`, `screenshots`, and `logs`.
- Writes Allure environment metadata to `reports/allure-results/environment.properties`.
- Starts Chrome or Edge before each scenario.
- Applies the implicit wait from config.
- Opens the configured base URL.
- Loads Excel test data into `context.test_data`.
- Captures screenshots for failed steps and failed scenarios.
- Quits the browser after each scenario.
- Attaches each scenario's log section to Allure.

### `features/`

The feature package contains BDD scenarios written in Gherkin:

- `positive_flows.feature`: valid search, 2 BHK filter, searched-location display, and property details validation.
- `negative_flows.feature`: shortlist requires login and empty-location search validation.
- `end_to_end.feature`: complete logged-in rental-property journey with search, filters, sorting, shortlist, owner details, and phone-number contact section validation.

### `features/steps/`

- `end_to_end_steps.py`: shared page-object helpers plus search, login, filter, property, shortlist, owner-contact, screenshot, and end-to-end steps.
- `positive_negative_steps.py`: additional assertions and steps for positive and negative feature scenarios.

### `pages/`

The `pages` package contains Page Object Model classes:

- `HomePage`: rent/buy tab actions, location entry, search submission, displayed location, and screenshots.
- `LoginPage`: profile hover, login/register popup, mobile-number entry, continue, OTP verify, and overlay handling.
- `SearchResultsPage`: result-page loading, heading validation, and result count extraction.
- `FiltersPage`: popup handling, filter application, sorting, visible result-card access, and first-property selection.
- `PropertyDetailsPage`: property-window switching, shortlist, owner details, phone/contact section, property title, and rent extraction.

### `locators/`

The `locators` package keeps Selenium locator definitions separate from page actions:

- `HomePageLocators`
- `LoginPageLocators`
- `SearchResultsPageLocators`
- `FiltersPageLocators`
- `PropertyDetailsPageLocators`

### `test_data/test_data.xlsx`

The workbook supplies runtime data for the BDD scenarios.

The current reader uses:

- Cell `A3` for `mobile_number`
- Cell `B2` for `location`

### `utilities/`

- `excel_reader.py`: reads `test_data/test_data.xlsx`.
- `logger.py`: configures file logging under `logs/automation.log`.

## Scenario Coverage

### Positive Scenarios

- Verify valid property search.
- Verify 2 BHK filter application.
- Verify searched location is displayed in the search bar.
- Verify property title and rent are visible on the property details page.

### Negative Scenarios

- Verify shortlist requires login.
- Verify submitting an empty location keeps the user on the same page.

### End-To-End Scenario

The tagged `@end_to_end` scenario validates the complete critical journey:

1. Login using the mobile number from Excel.
2. Wait for manual OTP entry.
3. Verify OTP and continue.
4. Search rental properties using the Excel location.
5. Validate the search results page.
6. Close blocking popups.
7. Apply filters: `2 BHK`, `Flat/Apartment`, `Owner`, `Single Men`.
8. Sort results by price low to high.
9. Validate required filters and visible results.
10. Open the first property.
11. Validate property title and rent.
12. Shortlist the property.
13. Open owner details.
14. View the phone number.
15. Validate the contact section.

This scenario includes a 20-second wait for manual OTP entry.

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Current dependencies are listed in `requirements.txt`:

```text
selenium
behave
webdriver-manager
allure-behave
pytest
openpyxl
configparser
gherkin-official
```

## Running Scenarios

Run all scenarios:

```powershell
.\.venv\Scripts\python.exe -m behave
```

Run all scenarios except the manual OTP end-to-end flow:

```powershell
.\.venv\Scripts\python.exe -m behave --tags "~@end_to_end"
```

Run only positive scenarios:

```powershell
.\.venv\Scripts\python.exe -m behave --tags "@positive"
```

Run only negative scenarios:

```powershell
.\.venv\Scripts\python.exe -m behave --tags "@negative"
```

Run only the end-to-end scenario:

```powershell
.\.venv\Scripts\python.exe -m behave --tags "@end_to_end"
```

Show plain console output for debugging:

```powershell
.\.venv\Scripts\python.exe -m behave --tags "~@end_to_end" -f plain
```

## Allure Reports

Behave is configured to write raw Allure results to:

```text
reports/allure-results/
```

To generate a fresh HTML report, install the Allure command-line tool separately, then run:

```powershell
allure generate reports\allure-results -o reports\allure-report --clean
```

To view the generated report locally:

```powershell
allure open reports\allure-report
```

## Logging And Screenshots

Runtime logs are written to:

```text
logs/automation.log
```

Screenshots are handled in two ways:

- Failed steps and failed scenarios are captured automatically by hooks in `features/environment.py`.
- Selected validation points capture screenshots through `HomePage.capture_screenshot()` and attach them to Allure.

Only Failed steps and failed scenarios are stored in screenshots folder:

```text
screenshots/
```

## Notes

- The end-to-end flow requires manual OTP entry within the configured wait time.
- The application under test is live, so locators and popups may need maintenance if the 99acres UI changes.
- `reports/`, `screenshots/`, and `logs/` are runtime output folders and can be regenerated by running the scenarios.

