"""upload_page.py
This page allows users to upload a pricing template in Excel format.
It processes the uploaded file and saves it as JSON files for different components.
It also displays the number of records for each component in the uploaded data.
It sets a session state variable to indicate that the upload was successful."""

import os
import streamlit as st
from utils.data_loader import process_excel_to_json

def render():
    st.header("Step 1: Upload Pricing Template")

    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

    if uploaded_file:
        filename = uploaded_file.name
        temp_path = os.path.join("parsed_data", filename)

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("📥 File uploaded! Parsing to JSON...")
        counts = process_excel_to_json(temp_path)

        st.success("✅ JSON files created in /data!")
        st.write("📊 Data Summary:")
        st.write(f"- Corrugate: `{counts['Corrugate']}` records")
        st.write(f"- EPE: `{counts['EPE']}` records")
        st.write(f"- MPP: `{counts['MPP']}` records")

        st.session_state["uploaded"] = True
