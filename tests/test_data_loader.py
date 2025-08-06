import os
import pandas as pd
from src.utils.data_loader import process_excel_to_json

def test_load_price_data_valid():
    # Replace with a real or mock Excel file path
    sample_file = "data/test_data.xlsx"
    if not os.path.exists(sample_file):
        # Create a minimal dummy Excel file for testing
        df = pd.DataFrame({"Type": ["Corrugate"], "Price": [10.5]})
        os.makedirs("tests/test_data", exist_ok=True)
        df.to_excel(sample_file, index=False)

    df_loaded = process_excel_to_json(sample_file)
    assert isinstance(df_loaded, pd.DataFrame)
    assert not df_loaded.empty
    assert "Type" in df_loaded.columns