import os

from openpyxl import load_workbook

def get_test_data():

    current_dir = os.path.dirname(__file__)

    file_path = os.path.join(
        current_dir,
        "..",
        "test_data",
        "test_data.xlsx"
    )

    workbook = load_workbook(file_path)

    sheet = workbook.active

    data = {
        "mobile_number": sheet["A3"].value,
        "location": sheet["B2"].value
    }

    return data
