"""
validate_multi_input.py

This script validates trained regression models (linear or SVR) for different packaging cost components,
including corrugate, EPE, MPP, and freight. It loads corresponding validation data, applies the trained model
to predict prices, computes the R² score, and visualizes the prediction performance against actual values.

Each prediction is plotted with a best-fit line using linear regression over the predicted values.
The resulting plot includes annotations, the regression equation, and is saved to a file for review.

Usage:
    python validate_multi_input.py --model [linear|svr] --component [corrugate|epe|mpp|freight]

Functions:
    - validate_model: Generates prediction plots with R² score and linear fit.
    - main: Handles data loading, model selection, and calls validation.
"""

import argparse

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from utils.data_loader import load_json
from utils.model_predictor import predict
from utils.utils import extract_xy, extract_xy_freight


def validate_model(X, y, labels, model_path, title, xlabel, ylabel, save_name):
    y_pred = predict(model_path, X)
    r2 = r2_score(y, y_pred)

    lin_reg = LinearRegression()
    lin_reg.fit(X, y_pred)
    a = lin_reg.coef_[0]
    b = lin_reg.intercept_
    equation = f"$y = {a:.4f}x + {b:.4f}$"

    plt.figure(figsize=(8, 6))
    plt.scatter(X, y, color="blue", label="Actual")

    sorted_idx = np.argsort(X.flatten())
    X_sorted = X[sorted_idx]
    y_pred_sorted = y_pred[sorted_idx]
    plt.plot(X_sorted, y_pred_sorted, color="red", linestyle="--", label="Prediction")

    plt.title(f"{title} (R² = {r2:.4f})")
    plt.xlabel(xlabel, size=18)
    plt.ylabel(ylabel, size=18)
    plt.legend()
    plt.grid(True)
    plt.text(
        0.05,
        0.95,
        equation,
        transform=plt.gca().transAxes,
        fontsize=12,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.6),
    )

    for i, label in enumerate(labels):
        plt.annotate(
            label,
            (X[i], y[i]),
            textcoords="offset points",
            xytext=(5, 2),
            ha="left",
            fontsize=8,
        )

    plt.tight_layout()
    plt.savefig(save_name)
    plt.close()


def main(component, model_type):

    if component == "corrugate":
        data = load_json("parsed_data/price_weight_corrugate.json")
        feature = "weight"
    elif component == "epe":
        data = load_json("parsed_data/price_weight_EPE.json")
        feature = "weight"
    elif component == "mpp":
        data = load_json("parsed_data/price_weight_MPP.json")
        feature = "weight"
    elif component == "freight":
        data = load_json("parsed_data/freight_cost_data.json")
        feature = "OD"
    elif component == "bag":
        data = load_json("parsed_data/price_size_bag.json")
        for item in data:
            item["area"] = item["l"] * item["h"]
        feature = "area"
    else:
        raise ValueError(f"Unsupported component: {component}")

    suffix = f"{model_type}_model"
    model_path = f"trained_models/{component}_{suffix}.pkl"
    save_path = f"validation_fig/validate_{component}_{suffix}.png"
    if component == "epe" or component == "mpp":
        title = f"{component.upper()} ({model_type.upper()})"
    else:
        title = f"{component.capitalize()} ({model_type.upper()})"

    if component == "freight":
        xlabel = "OD"
    elif component == "bag":
        xlabel = "Bag Area"
    else:
        xlabel = "Weight"

    ylabel = "price"
    if component == "freight":
        X, y = extract_xy_freight(data)
        labels = [""] * len(data)  # 或者根據需要加入 OD label
    else:
        X, y, labels = extract_xy(data, feature)

    validate_model(X, y, labels, model_path, title, xlabel, ylabel, save_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        choices=["linear", "svr"],
        required=True,
        help="Choose model type to validate",
    )
    parser.add_argument(
        "--component",
        choices=["corrugate", "epe", "mpp", "bag", "freight"],
        required=True,
        help="Component to validate",
    )
    args = parser.parse_args()
    main(args.component, args.model)
