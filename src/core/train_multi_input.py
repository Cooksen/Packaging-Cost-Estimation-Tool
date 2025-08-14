"""train_multi_input.py
This module contains the main function to train models for different components.
It supports both linear regression and support vector regression (SVR) models.
It can handle multiple components like corrugate, EPE, MPP, and freight.
The trained models are saved to specified paths for later use.
"""

import argparse
import logging

from models.regression import train_linear_model
from models.svr import train_svr_model
from utils.data_loader import load_json
from utils.utils import extract_xy, extract_xy_freight

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def get_data_by_component(component):
    if component == "corrugate":
        return load_json("parsed_data/price_weight_corrugate.json")
    elif component == "epe":
        return load_json("parsed_data/price_weight_EPE.json")
    elif component == "mpp":
        return load_json("parsed_data/price_weight_MPP.json")
    elif component == "freight":
        return load_json("parsed_data/freight_cost_data.json")
    elif component == "bag":
        return load_json("parsed_data/price_size_bag.json")
    else:
        raise ValueError(f"Unsupported component: {component}")


def train_model_for_component(component, model_type):
    logging.info(
        f"Starting training for component '{component}' with model '{model_type}'..."
    )
    data = get_data_by_component(component)

    if component == "freight":
        feature = "OD"
    elif component == "bag":
        for item in data:
            item["area"] = item["l"] * item["h"]
        feature = "area"
    else:
        feature = "weight"

    if component == "freight":
        X, y = extract_xy_freight(data)
    else:
        X, y, _ = extract_xy(data, feature=feature)

    if model_type == "linear":
        train_func = train_linear_model
        suffix = "linear_model"
    elif model_type == "svr":
        train_func = train_svr_model
        suffix = "svr_model"
    else:
        raise ValueError("Unsupported model type. Choose 'linear' or 'svr'.")

    model_path = f"trained_models/{component}_{suffix}.pkl"
    mse, r2 = train_func(X, y, model_path)
    return component, mse, r2


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        choices=["linear", "svr"],
        required=True,
        help="Choose which model to train",
    )
    parser.add_argument(
        "--component",
        choices=["corrugate", "epe", "mpp", "bag", "freight"],
        required=True,
        help="Component to train model for",
    )
    args = parser.parse_args()
    component, mse, r2 = train_model_for_component(args.component, args.model)
    logging.info(f"Training complete for '{component}'. MSE: {mse:.4f}, R²: {r2:.4f}")
