"""visualization_cli.py
This script runs the Streamlit application for the Packaging Cost Estimator.
It imports necessary modules and renders the main pages of the application.
"""

import subprocess


def main():
    subprocess.run(["streamlit", "run", "src/cli/run_app.py"])
