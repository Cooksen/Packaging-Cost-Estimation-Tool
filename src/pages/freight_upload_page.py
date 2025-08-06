"""freight_upload_page.py
This page allows users to upload freight cost data in Excel format.
It processes the uploaded file and saves it as a JSON file for further use.
It also displays the total number of records in the uploaded data."""

import os

import pandas as pd
import streamlit as st


def render():
    st.header("Step 2: Upload Freight Cost Estimator Data")

    uploaded_file = st.file_uploader(
        "Upload your Freight Cost Excel file", type=["xlsx"], key="freight_upload"
    )

    if uploaded_file:
        filename = uploaded_file.name
        temp_path = os.path.join("data", filename)

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("📥 Freight cost data uploaded successfully!")
        st.session_state["freight_data_path"] = temp_path

        # 顯示總筆數並儲存為 JSON
        try:
            df = pd.read_excel(temp_path, engine="openpyxl")
            st.write(f"📊 Total records in freight cost data: `{len(df)}`")

            # 儲存為 JSON
            json_path = "data/freight_cost_data.json"
            df.to_json(json_path, orient="records", indent=2)
            st.success(f"✅ JSON file saved to `{json_path}`")
        except Exception as e:
            st.error(f"❌ Failed to read freight cost data: {e}")
