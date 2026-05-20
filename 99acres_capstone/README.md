# 99acres Selenium Automation Framework

This project is a Python-based UI automation framework for the 99acres real estate website. It uses Selenium WebDriver, Pytest, the Page Object Model, Excel-driven test data, logging, screenshots, and Allure reporting to validate rental-property search flows.

The current framework focuses on the rent journey: opening 99acres, searching for rental properties by location, validating search results, applying filters, sorting by price, opening a property detail page, validating property details, and checking login/contact related behavior.

## Tech Stack

- Python 3.x
- Selenium WebDriver
- Pytest
- WebDriver Manager / Selenium driver management
- Allure Pytest integration
- OpenPyXL for Excel test data
- Chrome by default, with partial Edge support in the fixture

## Project Structure

```text
99acres_capstone/
|-- config/
|   |-- config.ini
|   `-- __init__.py
|-- pages/
|   |-- home_page.py
|   |-- login_page.py
|   |-- search_results_page.py
|   |-- filters_page.py
|   |-- property_details_page.py
|   `-- __init__.py
|-- tests/
|   |-- test_cases.py
|   |-- test_end_to_end_flow.py
|   `-- __init__.py
|-- test_data/
|   `-- search_data.xlsx
|-- utilities/
|   |-- config_reader.py
|   |-- excel_reader.py
|   |-- logger.py
|   `-- __init__.py
|-- allure-results/
|-- reports/allure-report/
|-- screenshots/
|-- logs/
|-- 99acres_Automation_Project_Documentation.docx
|-- conftest.py
|-- pytest.ini
|-- requirements.txt
`-- README.md
```


## Core Flow

1. `conftest.py` creates the browser fixture.
2. The fixture reads browser, base URL, and wait values from `config/config.ini`.
3. Tests load data from `test_data/search_data.xlsx` through `utilities/excel_reader.py`.
4. Test methods call page objects from `pages/`.
5. Page objects perform Selenium actions and validations.
6. Logs are written to `logs/automation.log`.
7. Failed tests save screenshots in `screenshots/`.
8. Allure result files are written to `allure-results/`.
9. A generated Allure HTML report can be stored in `reports/allure-report/`.

## Important Files

### `conftest.py`

Defines the shared `driver` fixture. It:

- Reads the configured browser.
- Launches Chrome or Edge.
- Applies Chrome options to reduce automation detection.
- Maximizes the browser window.
- Applies the implicit wait from config.
- Opens the configured base URL.
- Quits the browser after each test.
- Captures a screenshot automatically when a test fails.

### `config/config.ini`

Default runtime configuration:

```ini
[DEFAULT]
base_url = https://www.99acres.com
browser = chrome
implicit_wait = 15
```

Supported browser values in the fixture are `chrome` and `edge`.

### `pages/`

The `pages` package contains Page Object Model classes:

- `HomePage`: rent/buy tab selection, location entry, search submission, displayed location validation.
- `LoginPage`: profile hover, login/register popup, mobile number entry, continue/verify actions.
- `SearchResultsPage`: result page loading, heading validation, result count extraction.
- `FiltersPage`: popup handling, filter application, sorting, result-card access, first-property selection.
- `PropertyDetailsPage`: property-window switching, shortlist, owner details, phone/contact section, title and rent extraction.

### `tests/test_cases.py`

Contains independent positive and negative test cases:

- Valid property search.
- 2 BHK filter validation.
- Searched location displayed in the search bar.
- Property details page validation.
- Shortlist requires login.
- Empty location validation.

### `tests/test_end_to_end_flow.py`

Contains the full critical journey:

1. Login using mobile number.
2. Wait for manual OTP entry.
3. Search rental properties.
4. Validate search results.
5. Apply filters: `2 BHK`, `Flat/Apartment`, `Owner`, `Single Men`.
6. Sort by price low to high.
7. Open the first filtered property.
8. Shortlist property.
9. Open owner details.
10. View phone number.
11. Validate contact section, property title, and rent.

This test includes a fixed 25-second wait for manual OTP entry.

### `utilities/`

- `config_reader.py`: reads `config/config.ini`.
- `excel_reader.py`: reads `test_data/search_data.xlsx`.
- `logger.py`: configures console and file logging.

### `test_data/search_data.xlsx`

The workbook contains columns:

- `mobile_number`
- `location`

The current reader uses the first data row only: cell `A2` for `mobile_number` and cell `B2` for `location`.

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
pytest
webdriver-manager
allure-pytest
openpyxl
```

## Running Tests

Run all configured tests:

```powershell
pytest
```

Run with Allure result output:

```powershell
pytest --alluredir=allure-results
```

Run the independent test suite:

```powershell
pytest tests/test_cases.py
```

Run only the end-to-end flow:

```powershell
pytest tests/test_end_to_end_flow.py --alluredir=allure-results
```

The project has `pytest.ini` configured with:

```ini
addopts = -v -s
testpaths = tests
python_files = test_*.py
```

## Allure Reports

The repository already contains generated Allure result/report artifacts:

- `allure-results/`: raw Allure JSON, text, and PNG attachments.
- `reports/allure-report/`: generated static Allure HTML report.

To generate a fresh report, install the Allure command-line tool separately, then run:

```powershell
allure generate allure-results -o reports/allure-report --clean
```

To view the report locally:

```powershell
allure open reports/allure-report
```


## Logging And Screenshots

Runtime logs are written to:

```text
logs/automation.log
```

Screenshots are handled in two ways:

- Failed tests are captured automatically by the Pytest hook in `conftest.py`.
- Some tests attach screenshots directly to Allure using `capture_screenshot()`.

Saved screenshot files are stored in:

```text
screenshots/
```

## Notes And Limitations

- The automation depends on the live 99acres website, so DOM changes, popups, anti-bot behavior, or network issues can affect stability.
- The end-to-end test requires manual OTP entry and pauses for 25 seconds.
- `excel_reader.py` currently reads only one row from the Excel file, even though the workbook contains multiple data rows.
- `requirements.txt` does not pin package versions.
- The Allure CLI is not included by `allure-pytest`; install it separately if you want to generate/open HTML reports from the command line.
- The project contains generated artifacts such as reports, screenshots, caches, and local IDE/environment files. These are useful for review but are not source logic.




