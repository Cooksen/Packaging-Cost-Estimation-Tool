"""data_loader.py
This module contains functions to load data from JSON and CSV files.
It provides utilities to read and parse data for cost estimation tasks.
"""
"""load_price_template.py
This module contains a function to process an Excel file and convert it into JSON files for different components.
It extracts data for corrugate, EPE, MPP, and freight components and saves them in a structured format.
It also returns the number of records for each component in the uploaded data.
"""

import json
import pandas as pd
import openpyxl

def load_json(path):
    """
    Load a JSON file from the specified path.

    Args:
        path (str): The path to the JSON file.

    Returns:
        dict: The loaded JSON data.
    """
    with open(path, "r") as file:
        data = json.load(file)
    return data

def process_excel_to_json(file_path):
    wb = openpyxl.load_workbook(file_path, data_only=True)
    ws = wb.active
    headers = [cell.value for cell in ws[1]]

    corrugate_data, epe_data, mpp_data = [], [], []

    for row in ws.iter_rows(min_row=2, values_only=True):
        row_dict = dict(zip(headers, row))
        material = row_dict.get("material", "")
        if material is not None:
            material = material.strip().lower()
            if material == "corrugate":
                corrugate_data.append(row_dict)
            elif material == "epe":
                epe_data.append(row_dict)
            elif material == "mpp":
                mpp_data.append(row_dict)

    # Dump JSON files
    with open("parsed_data/price_weight_corrugate.json", "w", encoding="utf-8") as f:
        json.dump(corrugate_data, f, ensure_ascii=False, indent=2)
    with open("parsed_data/price_weight_EPE.json", "w", encoding="utf-8") as f:
        json.dump(epe_data, f, ensure_ascii=False, indent=2)
    with open("parsed_data/price_weight_MPP.json", "w", encoding="utf-8") as f:
        json.dump(mpp_data, f, ensure_ascii=False, indent=2)
    with open("parsed_data/freight.json", "w", encoding="utf-8") as f:
        json.dump(mpp_data, f, ensure_ascii=False, indent=2)

    # 回傳筆數資訊
    return {
        "Corrugate": len(corrugate_data),
        "EPE": len(epe_data),
        "MPP": len(mpp_data),
    }
