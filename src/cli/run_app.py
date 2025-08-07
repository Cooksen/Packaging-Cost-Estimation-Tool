"""run_app.py
This script runs the Streamlit application for the Packaging Cost Estimator.
It imports necessary modules and renders the main pages of the application.
"""

import streamlit as st

from pages import (estimate_page, freight_upload_page, train_validate_page,
                   upload_page)

st.set_page_config(page_title="Packaging Cost Estimator", layout="wide")
st.title("📦 Packaging Cost Estimator")

# Render three steps in one page (top to bottom)
upload_page.render()
st.markdown("---")
freight_upload_page.render()
st.markdown("---")
train_validate_page.render()
st.markdown("---")
estimate_page.render()
