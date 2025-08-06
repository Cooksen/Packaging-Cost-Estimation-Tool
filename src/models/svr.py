"""svr.py
This module contains the implementation of the Support Vector Regression (SVR) model.
It includes a function to train the SVR model and save it to a specified path.
It calculates and prints the training loss (MSE) and R² score."""

import joblib
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.svm import SVR


def train_svr_model(X, y, save_path):
    model = SVR(kernel="rbf", C=50, gamma=0.5, epsilon=0.5)
    model.fit(X.reshape(-1, 1), y)

    # 預測並計算 loss
    predictions = model.predict(X.reshape(-1, 1))
    loss = mean_squared_error(y, predictions)
    r2 = r2_score(y, predictions)
    print(f"Training loss (MSE): {loss:.4f}")

    # 儲存模型
    joblib.dump(model, save_path)
    print(f"Model saved to {save_path}")
    return loss, r2
