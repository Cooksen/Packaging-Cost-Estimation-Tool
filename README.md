# Packaging Cost Estimation System

This project provides a modular, extensible system for estimating the costs of packaging materials such as Corrugate, EPE, MPP, and Freight. It supports multi-model training (Linear, SVR), prediction, and a Streamlit UI interface.

---

## Features

- Excel-based pricing template ingestion
- Streamlit-based interactive interface
- Train & validate models with `linear` or `svr` options
- Predict cost per component using saved models
- Automated linting, formatting, and testing via `taskipy`

---

## Requirements

- Python 3.11+
- Poetry 1.7+
- Optional: Node.js if using advanced Streamlit components

---

## Installation

Install dependencies via Poetry:

```bash
poetry install
```

Activate the virtual environment:

```bash
poetry shell
```

---

## ️Usage

### Train & Validate Models

```bash
poetry run train          # Train using linear model
poetry run validate       # Validate linear model
poetry run train_svr      # Train using SVR model
poetry run validate_svr   # Validate SVR model
```

### Visualization (Command Line)

```bash
poetry run visualization
```

---

## Testing

Run all unit tests using pytest:

```bash
poetry run pytest tests/
```

---

## Formatting

### Format

```bash
poetry run task format
```

> These tasks are defined under `[tool.taskipy.tasks]` in `pyproject.toml`.

---

## Project Structure

```
src/
├── core/              # Training, validation, and inference logic
├── cli/               # Optional CLI wrappers (e.g. visualization)
├── models/            # Linear / SVR models
├── pages/             # Streamlit UI pages
├── utils/             # Data loading, predictors, config files
tests/
├── test_data_loader.py
├── test_model_predictor.py
└── test_train.py
```

---