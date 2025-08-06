"""model_predictor.py
This module provides a function to load a trained model and make predictions.
It supports both single value and array inputs for prediction.
The predicted price is returned as a float value.
"""

import joblib
import numpy as np

def predict(model_path, value):
    """
    Load a model from the specified path and make a prediction based on the input value.

    Args:
        model_path (str): The path to the model file.
        value (float): The input value for prediction.

    Returns:
        float: The predicted price.
    """
    model = joblib.load(model_path)
    if isinstance(value, (int, float)):
        value = np.array([[value]])
    elif isinstance(value, np.ndarray) and value.ndim == 1:
        value = value.reshape(-1, 1)

    return model.predict(value)
