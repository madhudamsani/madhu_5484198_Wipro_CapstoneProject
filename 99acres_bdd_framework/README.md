# 99acres BDD Framework

BDD automation framework for 99acres rental property flows using Behave,
Selenium, Page Object Model classes, Excel test data, logging, screenshots,
and Allure reporting.

## Project Structure

- `features/` contains Gherkin feature files and step definitions.
- `pages/` contains page object classes and locators.
- `utilities/` contains reusable logger and Excel reader helpers.
- `config/` contains project configuration.
- `test_data/` contains Excel input data.
- `reports/` contains Allure result and report output folders.
- `screenshots/` contains failure screenshots.
- `logs/automation.log` contains execution logs.

## Commands

Run all scenarios except the end-to-end OTP flow:

```powershell
.\.venv\Scripts\python.exe -m behave --tags "~@end_to_end"
```

Run all scenarios:

```powershell
.\.venv\Scripts\python.exe -m behave
```

Generate Allure results:

```powershell
.\.venv\Scripts\python.exe -m behave
```

Show plain console output for debugging:

```powershell
.\.venv\Scripts\python.exe -m behave --tags "~@end_to_end" -f plain
```

Generate the HTML Allure report after a run:

```powershell
allure generate reports\allure-results -o reports\allure-report --clean
```
