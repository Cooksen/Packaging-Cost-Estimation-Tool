"""utils.py
This module contains utility functions for cost estimation.
It includes functions to parse plank sizes and extract features from data.
It also provides functions to extract features and labels for training models."""

import joblib
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

def parse_plank_size(size_str):
    """Parse plank size from a string."""
    try:
        w, h = map(int, size_str.lower().replace("mm", "").split("x"))
        return w * h / 1e6
    except ValueError:
        return 0.0


def extract_xy(data, feature="weight"):
    X = np.array([item[feature] for item in data]).reshape(-1, 1)
    y = np.array([item["price"] / item["qty"] for item in data])
    labels = [f"{item.get('LOB', '')} {item.get('label', '')}" for item in data]
    return X, y, labels


def extract_xy_freight(data):
    X = np.array([item["OD"] for item in data]).reshape(-1, 1)
    y = np.array([item["price"] for item in data])
    return X, y
