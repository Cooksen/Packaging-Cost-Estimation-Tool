import os
import json
import pandas as pd
from src.utils.data_loader import process_excel_to_json, process_freight_data

def test_process_excel_to_json(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    
    sample_file = tmp_path / "test_data.xlsx"
    data = {
        "material": ["corrugate", "epe", "mpp", "bag", "corrugate"],
        "weight": [1.0, 0.1, 0.5, None, 1.2],
        "price": [10, 20, 30, 40, 50],
        "qty": [1, 2, 3, 4, 5],
        "l": [None, None, None, 10, None],
        "h": [None, None, None, 20, None],
        "label": ["A", "B", "C", "D", "E"],
        "LOB": ["X", "Y", "Z", "W", "V"]
    }
    df = pd.DataFrame(data)
    df.to_excel(sample_file, index=False)

    if not os.path.exists("parsed_data"):
        os.mkdir("parsed_data")

    counts = process_excel_to_json(sample_file)

    assert isinstance(counts, dict)
    assert counts["Corrugate"] == 1
    assert counts["EPE"] == 1
    assert counts["MPP"] == 1
    assert counts["Bag"] == 1

    corrugate_path = tmp_path / "parsed_data" / "price_weight_corrugate.json"
    assert os.path.exists(corrugate_path)
    with open(corrugate_path, 'r', encoding='utf-8') as f:
        corrugate_data = json.load(f)
    assert len(corrugate_data) == 1
    assert corrugate_data[0]['weight'] == 1.0


def test_process_freight_data(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    sample_file = tmp_path / "test_freight_data.xlsx"
    data = {
        "OD": [0.1, 0.2, 0.3],
        "price": [100, 200, 300]
    }
    df = pd.DataFrame(data)
    df.to_excel(sample_file, index=False)

    if not os.path.exists("parsed_data"):
        os.mkdir("parsed_data")

    output_json_path = tmp_path / "parsed_data" / "freight_cost_data.json"

    count = process_freight_data(sample_file)

    assert count == 3
    assert os.path.exists(output_json_path)
    with open(output_json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    assert len(json_data) == 3
    assert json_data[0]["OD"] == 0.1