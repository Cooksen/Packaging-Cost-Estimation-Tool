import numpy as np
import joblib
from sklearn.linear_model import LinearRegression
from src.utils.model_predictor import predict

def test_predict_model_output(tmp_path):
    X_train = np.array([[1], [2], [3]])
    y_train = np.array([2, 4, 6])
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    model_path = tmp_path / "test_model.pkl"
    joblib.dump(model, model_path)

    single_value_prediction = predict(model_path, 4)
    assert isinstance(single_value_prediction, np.ndarray)
    assert single_value_prediction.shape == (1,)
    np.testing.assert_almost_equal(single_value_prediction[0], 8.0)

    X_test = np.array([5, 6, 7])
    array_predictions = predict(model_path, X_test)
    assert isinstance(array_predictions, np.ndarray)
    assert array_predictions.shape == (3,)
    np.testing.assert_allclose(array_predictions, [10.0, 12.0, 14.0])

    X_test_2d = np.array([[8], [9]])
    array_2d_predictions = predict(model_path, X_test_2d)
    assert array_2d_predictions.shape == (2,)
    np.testing.assert_allclose(array_2d_predictions, [16.0, 18.0])