# Packaging Cost Estimation Tool

This project provides a modular, extensible system for estimating the costs of packaging materials (e.g., Corrugate, EPE, MPP) and freight. It features an interactive Streamlit UI, supports multiple regression models (`Linear`, `SVR`), and includes a suite of development tools for testing and code formatting.

## Features

- **Interactive UI**: A web-based interface built with Streamlit for easy data upload, model training, and cost estimation.
- **Excel-Based Data Ingestion**: Supports pricing and freight data import from `.xlsx` files.
- **Flexible Model Training**: Train and validate cost estimation models using Linear Regression or Support Vector Regression (SVR).
- **Component-Based Estimation**: Predict costs for individual packaging components and freight.
- **Developer Toolkit**: Integrated tasks for automated testing, code formatting, and import sorting.

## Requirements

- Python 3.11+
- Poetry 1.7+

## Installation

Use Poetry to install the required project dependencies.

```bash
poetry install
```

Activate the virtual environment:

```bash
poetry shell
```

## Usage

This project uses `poe the poet` as a task runner. All tasks are defined in the `pyproject.toml` file and can be executed with:

```bash
poetry run poe <task_name>
```

### Launch the Application

To start the Streamlit web application:

```bash
poetry run poe app
```

### Model Training & Validation (Command Line)

- **Train a Model**  
  Specify the `--model` (`linear` or `svr`) and `--component` (`corrugate`, `epe`, `mpp`, `bag`, `freight`):

```bash
# Example: Train the corrugate component with a linear model
poetry run poe train --model linear --component corrugate
```

- **Validate a Model**:

```bash
# Example: Validate the epe component with an SVR model
poetry run poe validate --model svr --component epe
```

### Development Tasks

- **Run Tests**:

```bash
poetry run poe test
```

- **Format Code**:

```bash
poetry run poe format
```

- **Sort Imports**:

```bash
poetry run poe isort
```

## Project Structure

```
src/
├── core/              # Core logic for training, validation, and inference
├── cli/               # Entry points for running the application
├── models/            # Linear Regression and SVR models
├── pages/             # Streamlit UI pages
├── utils/             # Utilities for data loading, prediction, etc.
tests/
├── test_data_loader.py
├── test_model_predictor.py
└── test_train.py
```
