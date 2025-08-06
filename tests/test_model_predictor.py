import numpy as np
from sklearn.linear_model import LinearRegression
from src.utils.model_predictor import predict

def test_predict_model_output_shape():
    X = np.random.rand(20, 4)
    y = np.random.rand(20)
    model = LinearRegression().fit(X, y)

    predictions = predict(model, X)
    assert predictions.shape == (20,)
    assert isinstance(predictions, np.ndarray)