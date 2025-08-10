"""freight_upload_page.py
This page allows users to upload freight cost data in Excel format.
It processes the uploaded file and saves it as a JSON file for further use.
It also displays the total number of records in the uploaded data.
"""

import os

import streamlit as st

from utils.data_loader import process_freight_data  # 確保路徑正確


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

        # 透過自訂的處理函式進行處理與儲存
        try:
            count = process_freight_data(temp_path)
            st.write("All records uploaded successfully!")
        except Exception as e:
            st.error(f"❌ Failed to process freight cost data: {e}")
